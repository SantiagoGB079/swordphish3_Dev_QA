package co.com.appgate.swordphish.models;

import java.util.List;

public class RequestMessage {

    private String correlationId;
    private String traceabilityId;
    private String replyTo;
    private List<String> urls;

    public void setUrls(List<String> urls) {
        this.urls = urls;
    }

    public String getCorrelationId() {
        return correlationId;
    }

    public String getTraceabilityId() {
        return traceabilityId;
    }

    public String getReplyTo() {
        return replyTo;
    }

    public List<String> getUrls() {
        return urls;
    }
}
