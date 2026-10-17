package com.minimaxflora.miniclash.service.models

data class NotificationParams(
    val title: String = "MiniClash",
    val stopText: String = "STOP",
    val onlyStatisticsProxy: Boolean = false,
    val showStopAction: Boolean = true,
)
