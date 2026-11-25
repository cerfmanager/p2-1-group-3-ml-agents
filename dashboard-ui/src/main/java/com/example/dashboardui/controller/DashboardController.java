package com.example.dashboardui.controller;

import com.example.dashboardui.model.Worker;
import com.example.dashboardui.service.ApiClient;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TableView;

import java.time.LocalDateTime;
import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.util.Duration;
import java.time.format.DateTimeFormatter;
import java.util.List;

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

    private final ApiClient apiClient = new ApiClient();

    @FXML
    public void initialize() {

        completedRunsLabel.setText("Completed: 53");
        runningRunsLabel.setText("Running: 4");
        assignedRunsLabel.setText("Assigned: 2");
        pendingRunsLabel.setText("Pending: 12");
        refreshData();
        startAutoRefresh();

    }


    @FXML
    private void refreshData() {

        updateLastRefresh();

        loadWorkers();

        loadRuns();
    }

    private void loadRuns() {
    }

    private void startAutoRefresh() {

        Timeline timeline = new Timeline(
            new KeyFrame(
                Duration.seconds(30),
                e -> refreshData()
            )
        );

        timeline.setCycleCount(
            Timeline.INDEFINITE
        );

        timeline.play();
    }

    private void updateLastRefresh() {

        DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("HH:mm:ss");

        lastRefreshLabel.setText(
            LocalDateTime.now()
                .format(formatter)
        );
    }

    private void loadWorkers() {
    /*
        List<Worker> workers =
            apiClient.getWorkers();

        workersTable.getItems().setAll(workers); */
    }

}
