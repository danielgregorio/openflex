// Explorer de Países com REST Countries API
// Consome API pública: https://restcountries.com

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

const API_URL = 'https://restcountries.com/v3.1';

// Fetch all countries
async function getAllCountries() {
    try {
        const response = await fetch(`${API_URL}/all`);
        return await response.json();
    } catch (error) {
        trace('Erro ao buscar países:', error.message);
        return [];
    }
}

// Fetch country by name
async function getCountryByName(name) {
    try {
        const response = await fetch(`${API_URL}/name/${name}`);
        return await response.json();
    } catch (error) {
        trace('Erro ao buscar país:', error.message);
        return [];
    }
}

// Fetch countries by region
async function getCountriesByRegion(region) {
    try {
        const response = await fetch(`${API_URL}/region/${region}`);
        return await response.json();
    } catch (error) {
        trace('Erro ao buscar região:', error.message);
        return [];
    }
}

// Display country info
function displayCountry(country) {
    trace(`\n${'═'.repeat(60)}`);
    trace(`🌍 ${country.name.common} (${country.cca2})`);
    trace(`${'═'.repeat(60)}`);

    trace(`\n📍 Nome Oficial: ${country.name.official}`);
    trace(`🏛️  Capital: ${country.capital ? country.capital[0] : 'N/A'}`);
    trace(`🌎 Região: ${country.region} - ${country.subregion || 'N/A'}`);
    trace(`👥 População: ${country.population.toLocaleString()}`);
    trace(`📏 Área: ${country.area.toLocaleString()} km²`);

    // Languages
    if (country.languages) {
        const langs = Object.values(country.languages).join(', ');
        trace(`🗣️  Idiomas: ${langs}`);
    }

    // Currencies
    if (country.currencies) {
        const currencies = Object.entries(country.currencies)
            .map(([code, curr]) => `${curr.name} (${curr.symbol})`)
            .join(', ');
        trace(`💰 Moedas: ${currencies}`);
    }

    // Timezone
    if (country.timezones) {
        trace(`🕐 Fusos: ${country.timezones.join(', ')}`);
    }

    // Borders
    if (country.borders && country.borders.length > 0) {
        trace(`🗺️  Fronteiras: ${country.borders.join(', ')}`);
    }

    trace(`🌐 Google Maps: ${country.maps.googleMaps}`);
}

// Display statistics
function displayStatistics(countries) {
    trace('\n\n📊 ESTATÍSTICAS GLOBAIS');
    trace('═'.repeat(60));

    const totalPop = countries.reduce((sum, c) => sum + (c.population || 0), 0);
    const totalArea = countries.reduce((sum, c) => sum + (c.area || 0), 0);

    trace(`\n🌍 Total de Países: ${countries.length}`);
    trace(`👥 População Mundial: ${totalPop.toLocaleString()}`);
    trace(`📏 Área Total: ${totalArea.toLocaleString()} km²`);

    // Top 5 mais populosos
    const top5Pop = countries
        .sort((a, b) => b.population - a.population)
        .slice(0, 5);

    trace('\n👥 Top 5 Mais Populosos:');
    top5Pop.forEach((c, i) => {
        trace(`  ${i + 1}. ${c.name.common.padEnd(20)} ${c.population.toLocaleString()}`);
    });

    // Top 5 maiores
    const top5Area = countries
        .sort((a, b) => b.area - a.area)
        .slice(0, 5);

    trace('\n📏 Top 5 Maiores (área):');
    top5Area.forEach((c, i) => {
        trace(`  ${i + 1}. ${c.name.common.padEnd(20)} ${c.area.toLocaleString()} km²`);
    });
}

// Main function
async function exploreCountries() {
    trace('=== 🌍 World Explorer OpenFlex ===');
    trace('Carregando dados da REST Countries API...\n');

    // Buscar países da América do Sul
    trace('🌎 Explorando América do Sul...\n');
    const southAmerica = await getCountriesByRegion('south america');

    // Mostrar alguns países
    const featured = ['Brazil', 'Argentina', 'Chile', 'Peru', 'Colombia'];

    for (const countryName of featured) {
        const countries = await getCountryByName(countryName);
        if (countries && countries.length > 0) {
            displayCountry(countries[0]);
        }
    }

    // Estatísticas da América do Sul
    if (southAmerica.length > 0) {
        trace('\n\n📊 ESTATÍSTICAS - AMÉRICA DO SUL');
        trace('═'.repeat(60));
        trace(`\n🌎 Países: ${southAmerica.length}`);
        const totalPop = southAmerica.reduce((sum, c) => sum + c.population, 0);
        trace(`👥 População Total: ${totalPop.toLocaleString()}`);
    }

    trace('\n\n✅ Exploração completa!');
    trace('💡 Visite https://restcountries.com para mais informações');
}

// Run
exploreCountries();
