package eu.dauphine;

public class AlertUid {
    public String uid;

    public AlertUid() {

    }
    public AlertUid(String uid) {
        this.uid = uid;
    }

    public String getUid() {
        return uid;
    }

    public void setUid(String uid) {
        this.uid = uid;
    }

    @Override
    public String toString() {

        return uid;
        /*
        return "Alert{" +
                "uid='" + uid + '\'' +
                '}';

         */
    }
}
