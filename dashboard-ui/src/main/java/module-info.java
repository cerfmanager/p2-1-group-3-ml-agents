module com.example.dashboardui {

    requires javafx.controls;
    requires javafx.fxml;

    exports com.example.dashboardui;

    exports com.example.dashboardui.model;
    exports com.example.dashboardui.service;

    opens com.example.dashboardui.controller to javafx.fxml;
}
