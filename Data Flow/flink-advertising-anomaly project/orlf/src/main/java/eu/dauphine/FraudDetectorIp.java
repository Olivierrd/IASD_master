package eu.dauphine;

import org.apache.flink.api.common.state.ListState;
import org.apache.flink.api.common.state.ListStateDescriptor;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.functions.KeyedProcessFunction;
import org.apache.flink.util.Collector;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Take as input the Event Stream (click or display) and return an Alert Stream of fraudulent IPs
 */
public class FraudDetectorIp extends KeyedProcessFunction<String, Event, AlertIp> {

    private static final int THRESHOLD = 10;

    private static final long serialVersionUID = 1L;

    /**
     * Count the number of clicks per ip every quarter-hour : save a list of timestamps of the clicks
     */
    private transient ListState<Long> clickState;
    /**
     * Count the number of displays per ip every quarter-hour : save a list of timestamps of the displays
     */
    private transient ListState<Long> displayState;

    //List of fraudulent IPs to remove
    private List<String> ip_to_remove = new ArrayList<>();

    @Override
    public void open(Configuration parameters) {
        ListStateDescriptor<Long> clickDescriptor = new ListStateDescriptor<>(
                "click",
                Types.LONG);
        clickState = getRuntimeContext().getListState(clickDescriptor);

        ListStateDescriptor<Long> displayDescriptor = new ListStateDescriptor<>(
                "display",
                Types.LONG);
        displayState = getRuntimeContext().getListState(displayDescriptor);
    }

    /**
     * Remove IPs which the number of clicks per quarter-hour is more than a threshold
     */
    @Override
    public void processElement(
            Event event,
            Context context,
            Collector<AlertIp> collector) throws Exception {

        if(event.getEventType().equals("click") || event.getEventType().equals("display")){

            if (event.getEventType().equals("click")) {clickState.add(event.getTimestamp()); }
            else {displayState.add(event.getTimestamp());}

            while(true) {
                Long _max_click; //max timestamp of click
                Long _min_click; //min timestamp of click
                Long _max_display; //max timestamp of display
                Long _min_display; //min timestamp of display

                if(((List)clickState.get()).size()==0) {
                    _max_click = 0L;
                    _min_click = 0L;
                } else {
                    _max_click = (Long) Collections.max((List) clickState.get());
                    _min_click = (Long) Collections.min((List) clickState.get());
                }

                if (((List)displayState.get()).size()==0) {
                    _max_display = 0L;
                    _min_display = 0L;
                } else {
                    _max_display = (Long) Collections.max((List) displayState.get());
                    _min_display = (Long) Collections.min((List) displayState.get());
                }

                /**
                 * Implementation of Session Windows
                 */
                if (_max_click - _min_click > 15 * 60 ||
                        _max_display - _min_display > 15 * 60) {

                    if (_max_click - _min_click > 15 * 60) {
                        List<Long> tmp = ((List<Long>) clickState.get());
                        tmp.remove(_min_click);
                        clickState.update(tmp); }

                    else {
                        List<Long> tmp = ((List<Long>) displayState.get());
                        tmp.remove(_min_display);
                        displayState.update(tmp);}

                } else {
                    int count = ((List<Long>) clickState.get()).size();
                    if (count > THRESHOLD) {

                        if(!ip_to_remove.contains(event.getIp())){
                            AlertIp alert = new AlertIp();
                            alert.setIp(event.getIp());
                            collector.collect(alert); //Send alert to the collector if never sent before
                            ip_to_remove.add(event.getIp());
                        }

                    }
                    break;
                }
            }
        }
    }
}