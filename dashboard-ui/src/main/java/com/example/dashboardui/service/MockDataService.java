package com.example.dashboardui.service;

import com.example.dashboardui.model.Metrics;
import com.example.dashboardui.model.Run;

import java.util.List;

public class MockDataService {

    public List<Run> getRuns() {

        return List.of(
            new Run(
                "baseline_rep_01",
                "baseline",
                null,
                null,
                1,
                "baseline.yaml",
                "completed",
                "worker-1"
            ),

            new Run(
                "beta_0p001_rep_01",
                "beta_0p001",
                "beta",
                0.001,
                1,
                "beta.yaml",
                "running",
                "worker-2"
            ),

            new Run(
                "beta_0p001_rep_02",
                "beta_0p001",
                "beta",
                0.001,
                2,
                "beta.yaml",
                "assigned",
                null
            )
        );
    }

    public Metrics getMetrics() {

        return new Metrics(
            12,
            4,
            53,
            0.76
        );
    }
}
