let page = 1;

function createPokeTemplate(pokemon) {
    const template = 
    <div class="border p-3 rounded-md hover:-translate-y-2 transition duration-300 transform">
    <div class="flex justify-between">
          <h1 class='text-xl font-semibold text-slate-900'>${pokemon.name}</h1>
          <form method="post" action="/delete">
            <input type="text" name="id" value="${pokemon.id}" hidden></input>
              
              <button class="w-8 h-8 bg-red-400	text-white rounded-full shadow" type="submit">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6 mx-auto">
                  <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                  </svg>

              </button>
          </form>
      </div>
      <img src="${pokemon.image_url}" alt="poke" class="min-h-52 object-cover rounded-md mx-auto" />

      <div class="grid grid-cols-2 gap-y-2 ">
          <span>
              <h2>Height: </h2>
              <p>${pokemon.height}</p>
          </span>
          <span>
              <h3>Weight: </h3>
              <p>${pokemon.weight}</p>
          </span>
          <span>
              <h2>Category: </h2>
              <p>${pokemon.category}</p>
          </span>
          <span>
              <h2>Abilities: </h2>
              <p>${pokemon.abilities}</p>
          </span>
      </div>
    </div>
    return template

}


function fetch_pokemons() {
    page = page + 1
    const url = `http://127.0.0.1:9000/get_pokemons?page=${page}`

    fetch(url)
    .then((resp) => resp.json() )
    .then((data) => {
        // logic to build the pokemon cards and append them to the page
        console.log(data);
        let card = document.querySelector('#poke-cards');

        data.forEach((pokemon) => {
            let template = createPokeTemplate(pokemon);
            card.innerHTML += template;
        });
        
    })
    .catch((error) => {
        console.log(error)
    });

}