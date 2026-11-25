package com.example.dashboardui.controller;

import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TableView;

import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;

public class DashboardController {

    public Button refreshButton;
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
    private Label lastRefreshLabel;

    @FXML
    public void initialize() {

        completedRunsLabel.setText("Completed: 53");
        runningRunsLabel.setText("Running: 4");
        assignedRunsLabel.setText("Assigned: 2");
        pendingRunsLabel.setText("Pending: 12");
        refreshData();
    }

    @FXML
    private void refreshData() {

        // API calls


        DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("HH:mm:ss");

        lastRefreshLabel.setText(
            LocalDateTime.now().format(formatter)
        );
    }
}
