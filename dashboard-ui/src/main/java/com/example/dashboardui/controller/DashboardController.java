package com.example.dashboardui.controller;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TableView;

public class DashboardController {

    @FXML
    private TableView<?> runsTable;

    @FXML
    private Label runningRunsLabel;

    @FXML
    private Label completedRunsLabel;

    @FXML
    private Label assignedRunsLabel;

    @FXML
    private Label pendingRunsLabel;

    @FXML
    public void initialize() {

        completedRunsLabel.setText("Completed: 53");
        runningRunsLabel.setText("Running: 4");
        assignedRunsLabel.setText("Assigned: 2");
        pendingRunsLabel.setText("Pending: 12");
    }
}
