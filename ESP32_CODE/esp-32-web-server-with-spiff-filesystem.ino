#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebSrv.h>
#include <SPIFFS.h>
#include <ArduinoJson.h>
#include <EEPROM.h>

// Replace with desired credentials for your ESP32 Access Point
const char* ssid     = "ESP32-Access-Point";
const char* password = "123456789";

IPAddress local_ip(192,168,4,1);
IPAddress gateway(192,168,4,1);
IPAddress subnet(255,255,255,0);

const int default_webserverporthttp = 80;

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML>
<html lang="en">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta charset="UTF-8">
</head>
<body>
  <p>Free Storage: %FREESPIFFS% | Used Storage: %USEDSPIFFS% | Total Storage: %TOTALSPIFFS%</p>
  <p>%FILELIST%</p>
</body>
</html>
)rawliteral";


AsyncWebServer *server;               // initialise webserver
File config_json;
const char *fileName = "/config.json";

void setup() {
  Serial.begin(115200);
  delay(500);
  EEPROM.begin(2048);
  Serial.println("Booting ...");

  Serial.println("Mounting SPIFFS ...");
  if (!SPIFFS.begin(true)) {
    // if you have not used SPIFFS before on a ESP32, it will show this error.
    // after a reboot SPIFFS will be configured and will happily work.
    Serial.println("ERROR: Cannot mount SPIFFS, Rebooting");
    rebootESP("ERROR: Cannot mount SPIFFS, Rebooting");
  }

  //Serial.print("SPIFFS Free: "); Serial.println(humanReadableSize((SPIFFS.totalBytes() - SPIFFS.usedBytes())));
  //Serial.print("SPIFFS Used: "); Serial.println(humanReadableSize(SPIFFS.usedBytes()));
  //Serial.print("SPIFFS Total: "); Serial.println(humanReadableSize(SPIFFS.totalBytes()));

  Serial.println(listFiles());

  Serial.println("\nLoading Configuration ...");
  
  Serial.print("Setting AP (Access Point)…");
  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig(local_ip, gateway, subnet);
  WiFi.softAP(ssid, password);
  
  Serial.print("AP IP address: ");
  Serial.println(WiFi.softAPIP());

  // configure web server
  Serial.println("\nConfiguring Webserver ...");
  server = new AsyncWebServer(default_webserverporthttp);
  configureWebServer();

  // startup web server
  Serial.println("Starting Webserver ...");
  server->begin();
}

void loop() {
}

void rebootESP(String message) {
  Serial.print("Rebooting ESP32: "); Serial.println(message);
  ESP.restart();
}

// list all of the files, if ishtml=true, return html rather than simple text
String listFiles() {
  String returnText = "";
  Serial.println("Listing files stored on SPIFFS");
  File root = SPIFFS.open("/");
  File foundfile = root.openNextFile();

  while (foundfile) {
    returnText += "File: " + String(foundfile.name()) + "\n";
    foundfile = root.openNextFile();
  }
  root.close();
  foundfile.close();
  return returnText;
}

// Make size of files human readable
// source: https://github.com/CelliesProjects/minimalUploadAuthESP32
String humanReadableSize(const size_t bytes) {
  if (bytes < 1024) return String(bytes) + " B";
  else if (bytes < (1024 * 1024)) return String(bytes / 1024.0) + " KB";
  else if (bytes < (1024 * 1024 * 1024)) return String(bytes / 1024.0 / 1024.0) + " MB";
  else return String(bytes / 1024.0 / 1024.0 / 1024.0) + " GB";
}

void configureWebServer() {
  server->on("/", HTTP_GET, [](AsyncWebServerRequest * request) {
    String logmessage = "Client:" + request->client()->remoteIP().toString() + + " " + request->url();
    Serial.println(logmessage);
    request->send_P(200, "text/html", index_html, processor);
  });

  server->on("/data", HTTP_GET, [](AsyncWebServerRequest * request) {
    String logmessage = "Receiving data ";
    const char *fileName = "/config.json";
    if (!SPIFFS.exists(fileName)) {
      Serial.println(logmessage + " ERROR: file does not exist");
      request->send(400, "text/plain", "ERROR: file does not exist");
    } else {
      Serial.println(logmessage + " file exists");
      
      logmessage += " downloaded";
      request->send(SPIFFS, fileName, "application/json");
      
      Serial.println(logmessage);
    }    
  });
  

  // run handleBody function
  server->on("/data", HTTP_POST, [](AsyncWebServerRequest *request) {
        request->send(200);
  }, NULL, handleBody);
}


void handleBody(AsyncWebServerRequest *request, uint8_t *data, size_t len, size_t index, size_t total){
 
  //String logmessage = "Writing data file size: " + String(total);

  if(!index){
    if (SPIFFS.exists(fileName)) {
      SPIFFS.remove(fileName);
    }
    //logmessage += "Write Start: " + String(fileName);
    config_json = SPIFFS.open(fileName, "w");
    //Serial.println(logmessage);
  }
  if (len) {
    config_json.write(data, len);
    //logmessage = "Writing file: " + String(fileName) + " index=" + String(index) + " len=" + String(len);
    //Serial.println(logmessage);
  }
  if(index + len == total){
    //logmessage = "Write Complete: " + String(fileName) + ",size: " + String(index + len);
    config_json.close();
    //Serial.println(logmessage);
    save_to_eeprom();
  }
}

String processor(const String& var) {
  if (var == "FILELIST") {
    return listFiles();
  }
  
  if (var == "FREESPIFFS") {
    return humanReadableSize((SPIFFS.totalBytes() - SPIFFS.usedBytes()));
  }

  if (var == "USEDSPIFFS") {
    return humanReadableSize(SPIFFS.usedBytes());
  }

  if (var == "TOTALSPIFFS") {
    return humanReadableSize(SPIFFS.totalBytes());
  }

  return String();
}


void save_to_eeprom(){
  File saved_json = SPIFFS.open(fileName, "r");
  Serial.println("Read from stored JSON");
  DynamicJsonDocument doc(81920);
  deserializeJson(doc, saved_json);

  for (JsonArray array1 : doc.as<JsonArray>())
  {
      int array_size = array1.size();
      if(array_size == 5){
        for(JsonArray array2:array1)
        {          
            for(JsonVariant v : array2)
            {
              int addr = v["addr"];
              String value = v["value"];
              
              if(!isDigit(value.charAt(0))){       // Text Label
                char text_label[10];
                strcpy(text_label, value.c_str());
                EEPROM.put(addr, text_label);
              }
              else {                              // Numeric Value
                int int_value = v["value"];
                EEPROM.write(addr, int_value );
              }
              //Serial.println(addr);
            }
        }
      }

      if(array_size == 4){
        for(JsonVariant v : array1){
          int addr = v["addr"];
          String value = v["value"];
                
          if(!isDigit(value.charAt(0))){       // Text Label
            char text_label[10];
            strcpy(text_label, value.c_str());
            EEPROM.put(addr, text_label);
          }
          else {                              // Numeric Value
            int int_value = v["value"];
            EEPROM.write(addr, int_value );
          }
          //Serial.println(addr);
        }
      }
  }
  saved_json.close();
  EEPROM.commit();
  //Serial.println("COMMIT TO EEPROM");
}
