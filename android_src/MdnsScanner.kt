package com.example.iothealth.network

import android.content.Context
import android.net.nsd.NsdManager
import android.net.nsd.NsdServiceInfo
import android.util.Log

class MdnsScanner(context: Context, private val onServiceFound: (String) -> Unit) {
    private val nsdManager = context.getSystemService(Context.NSD_SERVICE) as NsdManager

    private val discoveryListener = object : NsdManager.DiscoveryListener {
        override fun onDiscoveryStarted(regType: String) { Log.d("mDNS", "Discovery started") }
        override fun onServiceFound(service: NsdServiceInfo) {
            if (service.serviceName.contains("iot-health-monitor")) {
                nsdManager.resolveService(service, object : NsdManager.ResolveListener {
                    override fun onResolveFailed(serviceInfo: NsdServiceInfo, errorCode: Int) {}
                    override fun onServiceResolved(serviceInfo: NsdServiceInfo) {
                        val host = serviceInfo.host.hostAddress
                        onServiceFound("http://$host:8000")
                    }
                })
            }
        }
        override fun onServiceLost(service: NsdServiceInfo) {}
        override fun onDiscoveryStopped(regType: String) {}
        override fun onStartDiscoveryFailed(regType: String, errorCode: Int) { nsdManager.stopServiceDiscovery(this) }
        override fun onStopDiscoveryFailed(regType: String, errorCode: Int) { nsdManager.stopServiceDiscovery(this) }
    }

    fun start() { nsdManager.discoverServices("_http._tcp", NsdManager.PROTOCOL_DNS_SD, discoveryListener) }
    fun stop() { nsdManager.stopServiceDiscovery(discoveryListener) }
}
