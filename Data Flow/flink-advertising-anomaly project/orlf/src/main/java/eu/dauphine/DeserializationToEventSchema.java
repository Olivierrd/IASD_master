package eu.dauphine;

import org.apache.flink.api.common.serialization.AbstractDeserializationSchema;
import org.json.simple.parser.ParseException;
import java.nio.charset.StandardCharsets;

public class DeserializationToEventSchema extends AbstractDeserializationSchema<Event> {

        public Event deserialize(byte[] message) {
            String eventStr = new String(message, StandardCharsets.UTF_8);
            Event event = null;
            try {
                event = new Event(eventStr);
            } catch (ParseException e) {
                e.printStackTrace();
            }

            return event;
        }
}
