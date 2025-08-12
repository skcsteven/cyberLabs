# Why2025 Planets - Web 50

I just started programming and created my first website, an overview of all the planets in our solar system. Can you check if I didn't leave any security issues in it?

<img width="1920" height="1080" alt="Screenshot_2025-08-10_18_55_36" src="https://github.com/user-attachments/assets/253f3984-c347-441e-9557-dcaca9f8d05e" />

## Solution

When inspecting the html, there is an interesting fetch request that retrieves the planet information displayed on the page from an SQL database:

```

        try {
            fetch("/api.php", {
                method: "POST",
                body: "query=SELECT * FROM planets",
                headers: {"Content-type": "application/x-www-form-urlencoded; charset=UTF-8"},
            })
            .then(response => response.json())
            .then(response => addPlanets(response))
        } catch (error) {
            console.error(error.message);
        }
        
	function addPlanets(planets){

            let container  = document.getElementById("container");
            for (planet in planets){
                let div = document.createElement("div");
                div.classList = "planet";
    
                let h2 = document.createElement("h2");
                h2.textContent = planets[planet].name;
    
                let img = document.createElement("img");
                img.src = "images/" + planets[planet].image;
                img.alt = planets[planet].name;
    
                let p = document.createElement("p");
                p.textContent = planets[planet].description;
    
                div.appendChild(h2);
                div.appendChild(img);
                div.appendChild(p);
                container.appendChild(div);
            }
	}
    
```

From here, I try to enumerate the SQL server more and use the following as values for the "query" parameter:

```
SHOW DATABASES

SHOW TABLES
```
The results of the SHOW TABLES command displays the tables in the database:

<img width="1088" height="562" alt="image" src="https://github.com/user-attachments/assets/6aeb086a-9d22-4722-bfde-7d66a6805f65" />


There is an auspicious table on the database named "abandoned_planets", with the payload of "SELECT * FROM abandoned_planets" we capture the flag.

<img width="1220" height="729" alt="image" src="https://github.com/user-attachments/assets/9872ed78-5a84-4c81-b50b-67af656a44e7" />




