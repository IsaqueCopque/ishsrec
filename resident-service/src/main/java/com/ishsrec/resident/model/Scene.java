package com.ishsrec.resident.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "scenes")
public class Scene {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private Integer startTime; // 0-23

    @Column(nullable = false)
    private Integer endTime; // 0-23

    @Column(nullable = false)
    private boolean monday = false;

    @Column(nullable = false)
    private boolean tuesday = false;

    @Column(nullable = false)
    private boolean wednesday = false;

    @Column(nullable = false)
    private boolean thursday = false;

    @Column(nullable = false)
    private boolean friday = false;

    @Column(nullable = false)
    private boolean saturday = false;

    @Column(nullable = false)
    private boolean sunday = false;

    @Column(nullable = false)
    private String devicesIds;

    @ManyToOne
    @JoinColumn(name = "author_id", nullable = false)
    private Resident author;

    public Scene() {
    }

    public Scene(Integer startTime, Integer endTime, boolean monday, boolean tuesday, boolean wednesday,
                 boolean thursday, boolean friday, boolean saturday, boolean sunday, String devicesIds,
                 Resident author) {
        this.startTime = startTime;
        this.endTime = endTime;
        this.monday = monday;
        this.tuesday = tuesday;
        this.wednesday = wednesday;
        this.thursday = thursday;
        this.friday = friday;
        this.saturday = saturday;
        this.sunday = sunday;
        this.devicesIds = devicesIds;
        this.author = author;
    }

    public Long getId() {
        return id;
    }

    public Integer getStartTime() {
        return startTime;
    }

    public void setStartTime(Integer startTime) {
        this.startTime = startTime;
    }

    public Integer getEndTime() {
        return endTime;
    }

    public void setEndTime(Integer endTime) {
        this.endTime = endTime;
    }

    public boolean isMonday() {
        return monday;
    }

    public void setMonday(boolean monday) {
        this.monday = monday;
    }

    public boolean isTuesday() {
        return tuesday;
    }

    public void setTuesday(boolean tuesday) {
        this.tuesday = tuesday;
    }

    public boolean isWednesday() {
        return wednesday;
    }

    public void setWednesday(boolean wednesday) {
        this.wednesday = wednesday;
    }

    public boolean isThursday() {
        return thursday;
    }

    public void setThursday(boolean thursday) {
        this.thursday = thursday;
    }

    public boolean isFriday() {
        return friday;
    }

    public void setFriday(boolean friday) {
        this.friday = friday;
    }

    public boolean isSaturday() {
        return saturday;
    }

    public void setSaturday(boolean saturday) {
        this.saturday = saturday;
    }

    public boolean isSunday() {
        return sunday;
    }

    public void setSunday(boolean sunday) {
        this.sunday = sunday;
    }

    public String getDevicesIds() {
        return devicesIds;
    }

    public void setDevicesIds(String devicesIds) {
        this.devicesIds = devicesIds;
    }

    public Resident getAuthor() {
        return author;
    }

    public void setAuthor(Resident author) {
        this.author = author;
    }
}
