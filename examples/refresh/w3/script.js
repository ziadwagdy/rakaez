const temp = document.getElementById("temp");
const humidity = document.getElementById("humidity");
const water = document.getElementById("water");
const distance = document.getElementById("distance");
const tempCard = document.getElementById("temp-card");
const waterCard = document.getElementById("water-card");
const status = document.getElementById("status");

function updateReadings() {
  let temperature = Math.random() * 20 + 20;
  let humidityValue = Math.random() * 100;
  let waterLevel = Math.random() * 100;
  let distanceValue = Math.random() * 200;
  let alert = false;

  temp.textContent = temperature + " °C";
  humidity.textContent = humidityValue + " %";
  water.textContent = waterLevel + " %";
  distance.textContent = distanceValue + " cm";

  if (temperature > 30) {
    tempCard.style.backgroundColor = "#f85149";
    alert = true;
  } else {
    tempCard.style.backgroundColor = "#161b22";
  }

  if (waterLevel > 70) {
    waterCard.style.backgroundColor = "#f85149";
    alert = true;
  } else {
    waterCard.style.backgroundColor = "#161b22";
  }

  if (alert) {
    status.textContent = "⚠️ تنبيه";
  } else {
    status.textContent = "✅ الغرفة آمنة";
  }
  console.log(temperature);
}

updateReadings();
setInterval(updateReadings, 3000);
