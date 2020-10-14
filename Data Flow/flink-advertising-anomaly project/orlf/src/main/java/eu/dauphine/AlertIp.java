package eu.dauphine;

public class AlertIp {
    public String ip;

    public AlertIp() {

    }
    public AlertIp(String ip) {
        this.ip = ip;
    }

    public String getIp() {
        return ip;
    }

    public void setIp(String ip) {
        this.ip = ip;
    }

    @Override
    public String toString() {

        return ip;
        /*
        return "Alert{" +
                "ip='" + ip + '\'' +
                '}';

         */
    }
}
