xl = [
    {
        "name": "Kampala North"
    },
    {
        "name": "Lugogo"
    },
    {
        "name": "Mutundwe"
    },
    {
        "name": "Namungoona"
    },
    {
        "name": "Queens Way"
    }
]

xl.forEach(function (item) {
    item["name"] = item["name"].toLowerCase();
    console.log(item["name"]);
});
