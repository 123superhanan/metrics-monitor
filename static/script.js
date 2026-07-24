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

    service_name: document.getElementById("service_name").value,
    region: document.getElementById("region").value,
    deployment_version: document.getElementById("deployment_version").value,

    day_of_week: document.getElementById("day_of_week").value,
    hour: Number(document.getElementById("hour").value),
  };

  try {
    const [rfResponse, lstmResponse] = await Promise.all([
      fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }),

      fetch("http://127.0.0.1:8000/predict-lstm", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }),
    ]);

    const rfResult = await rfResponse.json();
    const lstmResult = await lstmResponse.json();

    document.getElementById("output").innerHTML = `

      <h3>Random Forest</h3>
      Prediction: ${rfResult.prediction}<br>
      Class: ${rfResult.class}


      <h3>LSTM</h3>
      Prediction: ${lstmResult.prediction}<br>
      Class: ${lstmResult.class ?? "Collecting sequence"}<br>
      Confidence: ${lstmResult.confidence ?? "N/A"}

    `;
  } catch (error) {
    document.getElementById("output").innerHTML = "API connection failed";

    console.log(error);
  }
}
