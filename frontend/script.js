window.onload = getCities;

async function addCity() {
    const cityName = document.getElementById("cityName").value;
    const latitude = parseFloat(document.getElementById("latitude").value);
    const longitude = parseFloat(document.getElementById("longitude").value);

    const response = await fetch("http://localhost:8000/cities/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name: cityName, latitude: latitude, longitude: longitude })
    });

    if (response.ok) {
        alert("City added successfully");
    } else {
        alert("Failed to add city");
    }
    getCities();
}

async function getCities() {
    const response = await fetch("http://localhost:8000/cities/");
    const cities = await response.json();

    const cityList = document.getElementById("cityList");
    cityList.innerHTML = "";

    cities.forEach(city => {
        const listItem = document.createElement("li");
        listItem.textContent = `${city.name} (${city.latitude}, ${city.longitude})`;
        cityList.appendChild(listItem);
    });
}


async function solveTSP() {
    const response = await fetch("http://localhost:8000/solve-tsp");
    const data = await response.json();

    // Отобразить результат на странице
    const tspCityList = document.getElementById("tspCityList");
    tspCityList.innerHTML = ""; // Очистить список перед добавлением новых городов
    data.order_of_travelling_names.forEach(city => {
        const listItem = document.createElement("li");
        listItem.textContent = city;
        tspCityList.appendChild(listItem);
    });
    const totalDistanceElement = document.getElementById("totalDistance");
    totalDistanceElement.textContent = `Total Distance: ${data.total_distance.toFixed(2)} units`;

    // Рисование маршрута на холсте
    const canvas = document.getElementById("mapCanvas");
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    const padding = 62; // отступ от краев холста
    const pointRadius = 11; // радиус точек

    const coords = data.order_of_travelling_coords; // данные с координатами
    const names = data.order_of_travelling_names; // данные с названиями городов

    // Вычисляем максимальные и минимальные значения координат точек
    const minX = Math.min(...coords.map(coord => coord[0]));
    const maxX = Math.max(...coords.map(coord => coord[0]));
    const minY = Math.min(...coords.map(coord => coord[1]));
    const maxY = Math.max(...coords.map(coord => coord[1]));

    // Определяем масштаб для отображения точек в пределах холста с учетом отступов
    const scaleX = (width - 2 * padding) / (maxY - minY);
    const scaleY = (height - 2 * padding) / (maxX - minX);

    // Очищаем холст
    ctx.clearRect(0, 0, width, height);

    // Отрисовываем линии маршрута
    ctx.beginPath();
    coords.forEach((coord, index) => {
        // Преобразование координат для поворота на 90 градусов влево и зеркального отображения
        const x = padding + (coord[1] - minY) * scaleX;
        const y = height - padding - (coord[0] - minX) * scaleY;
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.closePath();
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 2;
    ctx.stroke();

    // Отрисовываем точки и названия городов
    coords.forEach((coord, index) => {
        // Преобразование координат для поворота на 90 градусов влево и зеркального отображения
        const x = padding + (coord[1] - minY) * scaleX;
        const y = height - padding - (coord[0] - minX) * scaleY;
        ctx.beginPath();
        ctx.arc(x, y, pointRadius, 0, 2 * Math.PI);
        ctx.fillStyle = index === 0 ? "green" : "red"; // Первая точка зелёного цвета, остальные красного
        ctx.fill();
        ctx.strokeStyle = "black"; // Обводка черного цвета
        ctx.lineWidth = 1;
        ctx.stroke();
        ctx.closePath();

        // Добавляем названия городов рядом с точками
        ctx.font = "12px Arial";
        ctx.fillStyle = "black";
        ctx.fillText(names[index], x + pointRadius + 2, y - pointRadius - 2); // Смещение текста, чтобы он не перекрывал точку
    });
}




