package com.example.iothealth.viewmodel

import android.app.Application
import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.example.iothealth.data.SensorReading
import com.example.iothealth.network.ApiService
import com.example.iothealth.network.MdnsScanner
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class DashboardViewModel(application: Application) : AndroidViewModel(application) {
    private val _serverUrl = mutableStateOf<String?>(null)
    val serverUrl: State<String?> = _serverUrl

    private val _readings = MutableStateFlow<List<SensorReading>>(emptyList())
    val readings: StateFlow<List<SensorReading>> = _readings

    private val _isScanning = mutableStateOf(true)
    val isScanning: State<Boolean> = _isScanning

    private var apiService: ApiService? = null
    private val scanner = MdnsScanner(application) { url ->
        _serverUrl.value = url
        _isScanning.value = false
        setupRetrofit(url)
        startPolling()
    }

    init {
        scanner.start()
    }

    private fun setupRetrofit(url: String) {
        val retrofit = Retrofit.Builder()
            .baseUrl(url)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
        apiService = retrofit.create(ApiService::class.java)
    }

    private fun startPolling() {
        viewModelScope.launch {
            while (true) {
                try {
                    apiService?.let { service ->
                        val history = service.getHistory(20)
                        _readings.value = history
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
                delay(5000)
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        scanner.stop()
    }
}
