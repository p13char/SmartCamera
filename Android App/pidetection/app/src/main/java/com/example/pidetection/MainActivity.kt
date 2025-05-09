package com.example.pidetection


import android.app.AlertDialog
import android.net.Uri
import android.os.Bundle
import android.widget.TextView
import android.widget.VideoView
import androidx.appcompat.app.AppCompatActivity
import com.amazonaws.auth.BasicAWSCredentials
import com.amazonaws.services.s3.AmazonS3Client
import kotlinx.coroutines.*
import java.io.File
import java.net.URL

class MainActivity : AppCompatActivity() {

    private val bucketName = "picameradetection"
    private val accessKey = "*****"
    private val secretKey = "*****"
    private val region = "eu-north"
    private val videoFileName = "detection.mp4" // S3 object key
    private var lastModified: Long = 0 // Track the last modification time

    private lateinit var s3Client: AmazonS3Client
    private lateinit var statusTextView: TextView
    private lateinit var videoView: VideoView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize views
        statusTextView = findViewById(R.id.statusTextView)
        videoView = findViewById(R.id.videoView)

        // Initialize AWS S3 client
        val credentials = BasicAWSCredentials(accessKey, secretKey)
        s3Client = AmazonS3Client(credentials)

        // Start checking for file updates
        startPolling()
    }

    private fun startPolling() {
        CoroutineScope(Dispatchers.IO).launch {
            while (true) {
                try {
                    // Check the file's last modification time
                    val objectMetadata = s3Client.getObjectMetadata(bucketName, videoFileName)
                    val updatedTime = objectMetadata.lastModified.time

                    // If the file is updated
                    if (updatedTime > lastModified) {
                        lastModified = updatedTime
                        withContext(Dispatchers.Main) {
                            showNewFilePrompt()
                        }
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                    withContext(Dispatchers.Main) {
                        statusTextView.text = "Error checking S3: ${e.message}"
                    }
                }

                // Wait for 10 seconds before checking again
                delay(10000)
            }
        }
    }

    private fun showNewFilePrompt() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Person Detected")
        builder.setMessage("Click OK to watch the video.")
        builder.setPositiveButton("OK") { _, _ -> downloadAndPlayVideo() }
        builder.setNegativeButton("Cancel", null)
        builder.show()
    }

    private fun downloadAndPlayVideo() {
        CoroutineScope(Dispatchers.IO).launch {
            try {
                val file = File(cacheDir, videoFileName)
                val s3Object = s3Client.getObject(bucketName, videoFileName)
                s3Object.objectContent.use { inputStream ->
                    file.outputStream().use { outputStream ->
                        inputStream.copyTo(outputStream)
                    }
                }

                withContext(Dispatchers.Main) {
                    playVideo(file)
                }
            } catch (e: Exception) {
                e.printStackTrace()
                withContext(Dispatchers.Main) {
                    statusTextView.text = "Error downloading video: ${e.message}"
                }
            }
        }
    }

    private fun playVideo(file: File) {
        videoView.setVideoURI(Uri.fromFile(file))
        videoView.setOnPreparedListener { videoView.start() }
        videoView.setOnCompletionListener {
            statusTextView.text = "Video playback completed."
        }
    }
}
