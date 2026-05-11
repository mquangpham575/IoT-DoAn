package com.example.iothealth

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.iothealth.data.SensorReading
import com.example.iothealth.viewmodel.DashboardViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color(0xFF0F172A) // Match Web Dashboard BG
                ) {
                    DashboardScreen()
                }
            }
        }
    }
}

@Composable
fun DashboardScreen(viewModel: DashboardViewModel = viewModel()) {
    val readings by viewModel.readings.collectAsState()
    val serverUrl by viewModel.serverUrl
    val isScanning by viewModel.isScanning

    Column(modifier = Modifier.padding(16.dp)) {
        HeaderSection(serverUrl, isScanning)
        Spacer(modifier = Modifier.height(16.dp))
        
        if (readings.isNotEmpty()) {
            val current = readings.first()
            KpiGrid(current)
            Spacer(modifier = Modifier.height(16.dp))
            HistorySection(readings)
        } else {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text("Waiting for sensor data...", color = Color.White)
            }
        }
    }
}

@Composable
fun HeaderSection(url: String?, isScanning: Boolean) {
    Column {
        Text("Sentinel Mobile", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color.White)
        Text(
            text = if (isScanning) "Searching for server..." else "Connected: $url",
            fontSize = 14.sp,
            color = if (isScanning) Color.Yellow else Color.Green
        )
    }
}

@Composable
fun KpiGrid(reading: SensorReading) {
    Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            KpiCard("TEMP", "${reading.temp}°C", Modifier.weight(1f))
            KpiCard("HUMID", "${reading.humid}%", Modifier.weight(1f))
        }
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            KpiCard("GAS", "${reading.gas}ppm", Modifier.weight(1f))
            KpiCard("COMFORT", getComfortText(reading.comfort_level), Modifier.weight(1f))
        }
    }
}

@Composable
fun KpiCard(label: String, value: String, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B))
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(label, fontSize = 12.sp, color = Color(0xFF94A3B8), fontWeight = FontWeight.Bold)
            Text(value, fontSize = 20.sp, color = Color.White, fontWeight = FontWeight.Bold)
        }
    }
}

@Composable
fun HistorySection(readings: List<SensorReading>) {
    Text("RECENT HISTORY", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color(0xFF94A3B8))
    Spacer(modifier = Modifier.height(8.dp))
    LazyColumn(verticalArrangement = Arrangement.spacedBy(4.dp)) {
        items(readings) { reading ->
            HistoryItem(reading)
        }
    }
}

@Composable
fun HistoryItem(reading: SensorReading) {
    Card(
        colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(reading.timestamp.split(" ").last(), color = Color.White, fontSize = 12.sp)
            Text(
                getComfortText(reading.comfort_level),
                color = if (reading.comfort_level == 0) Color.Green else Color.Red,
                fontWeight = FontWeight.Bold,
                fontSize = 12.sp
            )
        }
    }
}

fun getComfortText(level: Int) = when(level) {
    0 -> "NORMAL"
    1 -> "WARNING"
    else -> "CRITICAL"
}
