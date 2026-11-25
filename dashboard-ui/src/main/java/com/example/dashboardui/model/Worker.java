package com.example.dashboardui.model;

public class Worker {
    private String machineId;
    private String status;
    private String lastSeen;

    public Worker(String machineId,
                  String status,
                  String lastSeen) {

        this.machineId = machineId;
        this.status = status;
        this.lastSeen = lastSeen;
    }

    public String getMachineId() {
        return machineId;
    }

    public String getStatus() {
        return status;
    }

    public String getLastSeen() {
        return lastSeen;
    }
}
