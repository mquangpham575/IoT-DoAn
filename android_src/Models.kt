package com.example.iothealth.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "sensors")
data class SensorReading(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val temp: Float,
    val humid: Float,
    val light: Float,
    val gas: Int,
    val noise: Int,
    val comfort_level: Int,
    val timestamp: String
)

data class SensorPayload(
    val temperature: Float,
    val humidity: Float,
    val light: Float,
    val gas: Int,
    val noise: Int
)
