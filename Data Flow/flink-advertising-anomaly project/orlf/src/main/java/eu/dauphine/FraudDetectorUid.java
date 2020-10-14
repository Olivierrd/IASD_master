package eu.dauphine;

import org.apache.flink.api.common.state.ListState;
import org.apache.flink.api.common.state.ListStateDescriptor;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Take as input the Event Stream (click or display) and return an Alert Stream of fraudulent UIDs
 */
public class FraudDetectorUid extends KeyedProcessFunction<String, Event, AlertUid> {

    private static final int THRESHOLD = 40;

    private static final long serialVersionUID = 1L;

    /**
     * Count the number of clicks per uid every quarter-hour : save a list of timestamps of the clicks
     */
    private transient ListState<Long> clickStateQuarter;
    /**
     * Count the number of clicks per uid every quarter-hour : save a list of timestamps of the clicks
     */
    private transient ListState<Long> displayStateQuarter;
    /**
     * Count the number of clicks per uid every hour : save a list of timestamps of the clicks
     */
    private transient ListState<Long> clickStateHour;
    /**
     * Count the number of displays per uid every hour : save a list of timestamps of the displays
     */
    private transient ListState<Long> displayStateHour;

    //List of fraudulent UIDs to remove
    private List<String> uids_to_remove;
    //Map each UID with their current CTR
    private Map<String,Float> map_uid_ctr;

    //first timestamp of events
    private long timestamp_start = (long) -1.0;
    //last timestamp of events
    private long timestamp_end = (long) -1.0;

    @Override
    public void open(Configuration parameters) {
        ListStateDescriptor<Long> clickDescriptorQuarter = new ListStateDescriptor<>(
                "click",
                Types.LONG);
        clickStateQuarter = getRuntimeContext().getListState(clickDescriptorQuarter);

        ListStateDescriptor<Long> displayDescriptorQuarter = new ListStateDescriptor<>(
                "display",
                Types.LONG);
        displayStateQuarter = getRuntimeContext().getListState(displayDescriptorQuarter);

        ListStateDescriptor<Long> clickDescriptorHour = new ListStateDescriptor<>(
                "click",
                Types.LONG);
        clickStateHour = getRuntimeContext().getListState(clickDescriptorHour);

        ListStateDescriptor<Long> displayDescriptorHour = new ListStateDescriptor<>(
                "display",
                Types.LONG);
        displayStateHour = getRuntimeContext().getListState(displayDescriptorHour);
    }

    /**
     * Remove UIDs which the number of clicks per quarter-hour is more than a threshold
     */
    @Override
    public void processElement(Event event,Context context,Collector<AlertUid> collector) throws Exception {

        //init variables
        if(timestamp_start <= 0.0) {
            timestamp_start = event.getTimestamp();
            uids_to_remove = new ArrayList<>();
            map_uid_ctr = new HashMap<>();
        }
        //update last timestamp
        if(timestamp_end <= event.getTimestamp()) {
            timestamp_end = event.getTimestamp();
        }
        //One-hour time's up : calculate a mean of CTR per UID
        if(timestamp_end-timestamp_start >= 15*60) {

            //filter the ctr of uids to remove
            Map<String, Float> result = map_uid_ctr.entrySet()
                    .stream()
                    .filter(map -> !uids_to_remove.contains(map.getKey()))
                    .collect(Collectors.toMap(map -> map.getKey(), map -> map.getValue()));

            //calculate mean CTR per UID
            double meanCTR = 0.0;

            for (String key : result.keySet() ){
                meanCTR+=result.get(key);
            }
            meanCTR /= result.size();
            System.out.println("####################### Mean CTR : " + meanCTR + " #######################");

            //reset timestamps
            timestamp_start = event.getTimestamp();
            timestamp_end = event.getTimestamp();

            map_uid_ctr = new HashMap<>();
        }

        if(event.getEventType().equals("display")) {
            displayStateQuarter.add(event.getTimestamp());
            displayStateHour.add(event.getTimestamp());

            while(true) {
                Long _maxHour = (Long) Collections.max((List) displayStateHour.get());
                Long _minHour = (Long) Collections.min((List) displayStateHour.get());

                if (_maxHour - _minHour > 60 * 60) {
                    displayStateHour.update(new ArrayList<>()); //reset
                } else {
                    break;
                }
            }

        }
        if(event.getEventType().equals("click")){
            clickStateQuarter.add(event.getTimestamp());
            clickStateHour.add(event.getTimestamp());

            while(true) {
                Long _maxQuarter = (Long) Collections.max((List) clickStateQuarter.get()); //max timestamp
                Long _minQuarter = (Long) Collections.min((List) clickStateQuarter.get()); //min timestamp

                /**
                 * Implementation of Session Windows
                 */
                if (_maxQuarter - _minQuarter > 15 * 60) {
                    List<Long> tmp = ((List<Long>) clickStateQuarter.get());
                    tmp.remove(_minQuarter);

                    clickStateQuarter.update(tmp);
                } else {
                    int count = ((List<Long>) clickStateQuarter.get()).size();

                    /**
                     *
                     * FIRST FRAUDULENT PATTERN : clicks without display
                     *
                     */

                    if (((List<Long>) clickStateQuarter.get()).size() > 0 && ((List<Long>) displayStateQuarter.get()).size() == 0) {
                        if(!uids_to_remove.contains(event.getUid())){
                            AlertUid alert = new AlertUid();
                            alert.setUid(event.getUid());
                            collector.collect(alert); //Send alert to the collector
                            uids_to_remove.add(event.getUid());
                        }
                    }

                    /**
                     *
                     * SECOND FRAUDULENT PATTERN : number of clicks too high per quarter-hour (THRESHOLD defined)
                     *
                     */
                    if (count > THRESHOLD){ //fraudulent UID
                        if(!uids_to_remove.contains(event.getUid())){
                            AlertUid alert = new AlertUid();
                            alert.setUid(event.getUid());
                            collector.collect(alert); //Send alert to the collector
                            uids_to_remove.add(event.getUid());
                        }

                    }
                    break;
                }
            }
        }

        //Save current CTR for the current UID
        int nbClicks = ((List) clickStateHour.get()).size();
        float nbDisplays = Math.max((float)((List) displayStateHour.get()).size(),(float)1.0);
        Float ctr = nbClicks/nbDisplays;
        map_uid_ctr.put(event.getUid(),ctr);
    }
}