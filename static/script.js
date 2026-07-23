async function predict() {
  const data = {
    cpu_usage: Number(document.getElementById("cpu_usage").value),
    memory_usage: Number(document.getElementById("memory_usage").value),
    disk_usage: Number(document.getElementById("disk_usage").value),
    disk_io: Number(document.getElementById("disk_io").value),

    network_in: Number(document.getElementById("network_in").value),
    network_out: Number(document.getElementById("network_out").value),

    response_time: Number(document.getElementById("response_time").value),
    request_count: Number(document.getElementById("request_count").value),

    error_rate: Number(document.getElementById("error_rate").value),
    active_users: Number(document.getElementById("active_users").value),

    service_name: Number(document.getElementById("service_name").value),
    region: Number(document.getElementById("region").value),
    deployment_version: Number(
      document.getElementById("deployment_version").value,
    ),

    day_of_week: Number(document.getElementById("day_of_week").value),
    hour: Number(document.getElementById("hour").value),
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    document.getElementById("output").innerHTML = `
            Prediction: ${result.prediction}<br>
            Class: ${result.class}
            `;
  } catch (error) {
    document.getElementById("output").innerHTML = "API connection failed";

    console.log(error);
  }
}
