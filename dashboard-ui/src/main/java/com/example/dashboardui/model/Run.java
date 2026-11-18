package com.example.dashboardui.model;

public class Run {

    private String runId;
    private String configId;
    private String hyperparameter;
    private Double value;
    private int repetition;
    private String yamlFile;
    private String status;
    private String machineId;

    public Run(
        String runId,
        String configId,
        String hyperparameter,
        Double value,
        int repetition,
        String yamlFile,
        String status,
        String machineId) {

        this.runId = runId;
        this.configId = configId;
        this.hyperparameter = hyperparameter;
        this.value = value;
        this.repetition = repetition;
        this.yamlFile = yamlFile;
        this.status = status;
        this.machineId = machineId;
    }

    public String getRunId() {
        return runId;
    }

    public String getConfigId() {
        return configId;
    }

    public String getHyperparameter() {
        return hyperparameter;
    }

    public Double getValue() {
        return value;
    }

    public int getRepetition() {
        return repetition;
    }

    public String getYamlFile() {
        return yamlFile;
    }

    public String getStatus() {
        return status;
    }

    public String getMachineId() {
        return machineId;
    }
}
