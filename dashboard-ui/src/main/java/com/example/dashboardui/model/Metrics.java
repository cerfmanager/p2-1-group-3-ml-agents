package com.example.dashboardui.model;

public class Metrics {

    private final int queuedRuns;
    private final int runningRuns;
    private final int completedRuns;
    private final double averageReward;

    public Metrics(
        int queuedRuns,
        int runningRuns,
        int completedRuns,
        double averageReward) {

        this.queuedRuns = queuedRuns;
        this.runningRuns = runningRuns;
        this.completedRuns = completedRuns;
        this.averageReward = averageReward;
    }

    public int getQueuedRuns() {
        return queuedRuns;
    }

    public int getRunningRuns() {
        return runningRuns;
    }

    public int getCompletedRuns() {
        return completedRuns;
    }

    public double getAverageReward() {
        return averageReward;
    }
}
