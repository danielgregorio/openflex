// Blog com JSONPlaceholder API
// Consome API pública: https://jsonplaceholder.typicode.com

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

// API Base URL
const API_URL = 'https://jsonplaceholder.typicode.com';

// Fetch posts
async function getPosts() {
    try {
        const response = await fetch(`${API_URL}/posts`);
        const posts = await response.json();
        return posts.slice(0, 10); // Primeiros 10 posts
    } catch (error) {
        trace('Erro ao buscar posts:', error.message);
        return [];
    }
}

// Fetch user by ID
async function getUser(userId) {
    try {
        const response = await fetch(`${API_URL}/users/${userId}`);
        return await response.json();
    } catch (error) {
        trace('Erro ao buscar usuário:', error.message);
        return null;
    }
}

// Fetch comments for a post
async function getComments(postId) {
    try {
        const response = await fetch(`${API_URL}/posts/${postId}/comments`);
        const comments = await response.json();
        return comments.slice(0, 3); // Primeiros 3 comentários
    } catch (error) {
        trace('Erro ao buscar comentários:', error.message);
        return [];
    }
}

// Display blog
async function displayBlog() {
    trace('=== 📝 Blog OpenFlex ===');
    trace('Carregando posts do JSONPlaceholder...\n');

    const posts = await getPosts();

    for (const post of posts) {
        trace(`\n${'='.repeat(60)}`);
        trace(`📄 Post #${post.id}: ${post.title}`);
        trace(`${'='.repeat(60)}`);
        trace(`\n${post.body}\n`);

        // Buscar autor
        const user = await getUser(post.userId);
        if (user) {
            trace(`👤 Autor: ${user.name} (@${user.username})`);
            trace(`📧 Email: ${user.email}`);
            trace(`🌐 Website: ${user.website}\n`);
        }

        // Buscar comentários
        const comments = await getComments(post.id);
        if (comments.length > 0) {
            trace(`💬 Comentários (${comments.length}):`);
            comments.forEach((comment, index) => {
                trace(`  ${index + 1}. ${comment.name}`);
                trace(`     Por: ${comment.email}`);
                trace(`     "${comment.body.substring(0, 80)}..."\n`);
            });
        }

        // Apenas mostrar 2 posts completos para não lotar o console
        if (post.id >= 2) {
            trace(`\n... e mais ${posts.length - 2} posts!\n`);
            break;
        }
    }

    trace('\n✅ Blog carregado com sucesso!');
}

// Run
displayBlog();
