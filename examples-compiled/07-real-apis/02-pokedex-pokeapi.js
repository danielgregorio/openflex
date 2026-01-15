// Pokédex com PokeAPI
// Consome API pública: https://pokeapi.co

const trace = typeof console !== 'undefined' ? console.log : () => {};

// Polyfill fetch for Node.js < 18
if (typeof fetch === 'undefined') {
    global.fetch = async (url) => {
        const https = require('https');
        return new Promise((resolve, reject) => {
            https.get(url, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    resolve({
                        ok: res.statusCode === 200,
                        json: async () => JSON.parse(data)
                    });
                });
            }).on('error', reject);
        });
    };
}

const API_URL = 'https://pokeapi.co/api/v2';

// Fetch pokemon by ID or name
async function getPokemon(idOrName) {
    try {
        const response = await fetch(`${API_URL}/pokemon/${idOrName}`);
        return await response.json();
    } catch (error) {
        trace('Erro ao buscar Pokemon:', error.message);
        return null;
    }
}

// Fetch pokemon species (for description)
async function getPokemonSpecies(id) {
    try {
        const response = await fetch(`${API_URL}/pokemon-species/${id}`);
        return await response.json();
    } catch (error) {
        return null;
    }
}

// Display pokemon info
async function displayPokemon(pokemon) {
    if (!pokemon) return;

    trace(`\n${'═'.repeat(60)}`);
    trace(`🎮 #${pokemon.id} - ${pokemon.name.toUpperCase()}`);
    trace(`${'═'.repeat(60)}`);

    // Stats
    trace('\n📊 Stats:');
    pokemon.stats.forEach(stat => {
        const barLength = Math.floor(stat.base_stat / 10);
        const bar = '█'.repeat(barLength) + '░'.repeat(15 - barLength);
        trace(`  ${stat.stat.name.padEnd(20)} ${bar} ${stat.base_stat}`);
    });

    // Types
    trace('\n🏷️  Tipos:', pokemon.types.map(t => t.type.name).join(', '));

    // Abilities
    trace('✨ Habilidades:', pokemon.abilities.map(a => a.ability.name).join(', '));

    // Physical info
    trace(`\n📏 Altura: ${pokemon.height / 10}m`);
    trace(`⚖️  Peso: ${pokemon.weight / 10}kg`);

    // Moves (primeiros 5)
    const moves = pokemon.moves.slice(0, 5).map(m => m.move.name);
    trace(`\n⚔️  Alguns Golpes: ${moves.join(', ')}...`);
}

// Main Pokedex
async function runPokedex() {
    trace('=== 🎮 Pokédex OpenFlex ===');
    trace('Carregando dados da PokeAPI...\n');

    // Buscar alguns pokemon famosos
    const pokemonList = [
        { id: 25, name: 'pikachu' },
        { id: 1, name: 'bulbasaur' },
        { id: 4, name: 'charmander' },
        { id: 7, name: 'squirtle' },
        { id: 150, name: 'mewtwo' }
    ];

    for (const { id, name } of pokemonList) {
        const pokemon = await getPokemon(name);
        await displayPokemon(pokemon);
    }

    trace('\n\n✅ Pokédex carregada com sucesso!');
    trace('💡 Visite https://pokeapi.co para mais informações');
}

// Run
runPokedex();
