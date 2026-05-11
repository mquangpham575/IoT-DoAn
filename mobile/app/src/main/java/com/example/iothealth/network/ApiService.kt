package com.example.iothealth.network

import com.example.iothealth.data.SensorReading
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {
    @GET("/history")
    suspend fun getHistory(@Query("limit") limit: Int): List<SensorReading>
    
    @GET("/")
    suspend fun getStatus(): Map<String, Any>
}
