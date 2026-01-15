#!/usr/bin/env node
/**
 * Mock API Server for OpenFlex E-Commerce Example

// Polyfill for Node.js
const trace = typeof console !== 'undefined' ? console.log : () => {};
 * Provides realistic REST API for development and testing
 */

const http = require('http');
const url = require('url');

const PORT = 3000;

// Mock Database
const db = {
    products: [
        {
            id: 1,
            name: "Wireless Headphones",
            description: "Premium noise-canceling wireless headphones with 30-hour battery life",
            price: 299.99,
            category: "Electronics",
            image: "https://via.placeholder.com/300x300?text=Headphones",
            stock: 15,
            rating: 5
        },
        {
            id: 2,
            name: "Smart Watch",
            description: "Fitness tracking smartwatch with heart rate monitor and GPS",
            price: 249.99,
            category: "Electronics",
            image: "https://via.placeholder.com/300x300?text=Smart+Watch",
            stock: 8,
            rating: 4
        },
        {
            id: 3,
            name: "Laptop Backpack",
            description: "Durable water-resistant backpack with laptop compartment",
            price: 79.99,
            category: "Accessories",
            image: "https://via.placeholder.com/300x300?text=Backpack",
            stock: 25,
            rating: 5
        },
        {
            id: 4,
            name: "Mechanical Keyboard",
            description: "RGB mechanical gaming keyboard with custom switches",
            price: 149.99,
            category: "Electronics",
            image: "https://via.placeholder.com/300x300?text=Keyboard",
            stock: 12,
            rating: 5
        },
        {
            id: 5,
            name: "Wireless Mouse",
            description: "Ergonomic wireless mouse with precision sensor",
            price: 59.99,
            category: "Electronics",
            image: "https://via.placeholder.com/300x300?text=Mouse",
            stock: 30,
            rating: 4
        },
        {
            id: 6,
            name: "USB-C Hub",
            description: "7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader",
            price: 49.99,
            category: "Accessories",
            image: "https://via.placeholder.com/300x300?text=USB+Hub",
            stock: 20,
            rating: 4
        },
        {
            id: 7,
            name: "Webcam 4K",
            description: "4K webcam with auto-focus and built-in microphone",
            price: 129.99,
            category: "Electronics",
            image: "https://via.placeholder.com/300x300?text=Webcam",
            stock: 10,
            rating: 5
        },
        {
            id: 8,
            name: "Phone Stand",
            description: "Adjustable aluminum phone and tablet stand",
            price: 29.99,
            category: "Accessories",
            image: "https://via.placeholder.com/300x300?text=Phone+Stand",
            stock: 50,
            rating: 4
        }
    ],
    users: [
        {
            id: 1,
            email: "demo@openflex.org",
            password: "demo123",
            name: "Demo User",
            token: "demo-token-12345"
        }
    ],
    orders: []
};

// Helper functions
function sendJSON(res, statusCode, data) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    });
    res.end(JSON.stringify(data));
}

function parseBody(req, callback) {
    let body = '';
    req.on('data', chunk => body += chunk.toString());
    req.on('end', () => {
        try {
            callback(null, JSON.parse(body));
        } catch (e) {
            callback(e);
        }
    });
}

function getAuthUser(req) {
    const authHeader = req.headers['authorization'];
    if (!authHeader) return null;

    const token = authHeader.replace('Bearer ', '');
    return db.users.find(u => u.token === token);
}

// Request handler
function handleRequest(req, res) {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    const query = parsedUrl.query;
    const method = req.method;

    console.log(`${method} ${path}`);

    // CORS preflight
    if (method === 'OPTIONS') {
        sendJSON(res, 200, {});
        return;
    }

    // Routes
    if (path === '/api/products' && method === 'GET') {
        let products = db.products;

        // Filter by category
        if (query.category) {
            products = products.filter(p => p.category === query.category);
        }

        sendJSON(res, 200, { products });
        return;
    }

    if (path.match(/^\/api\/products\/\d+$/) && method === 'GET') {
        const id = parseInt(path.split('/').pop());
        const product = db.products.find(p => p.id === id);

        if (product) {
            sendJSON(res, 200, { product });
        } else {
            sendJSON(res, 404, { error: 'Product not found' });
        }
        return;
    }

    if (path === '/api/products/search' && method === 'GET') {
        const q = (query.q || '').toLowerCase();
        const products = db.products.filter(p =>
            p.name.toLowerCase().includes(q) ||
            p.description.toLowerCase().includes(q)
        );

        sendJSON(res, 200, { products });
        return;
    }

    if (path === '/api/auth/login' && method === 'POST') {
        parseBody(req, (err, body) => {
            if (err) {
                sendJSON(res, 400, { error: 'Invalid JSON' });
                return;
            }

            const user = db.users.find(u =>
                u.email === body.email && u.password === body.password
            );

            if (user) {
                const { password, ...userData } = user;
                sendJSON(res, 200, { user: userData });
            } else {
                sendJSON(res, 401, { error: 'Invalid credentials' });
            }
        });
        return;
    }

    if (path === '/api/auth/register' && method === 'POST') {
        parseBody(req, (err, body) => {
            if (err) {
                sendJSON(res, 400, { error: 'Invalid JSON' });
                return;
            }

            // Check if email exists
            if (db.users.find(u => u.email === body.email)) {
                sendJSON(res, 409, { error: 'Email already registered' });
                return;
            }

            // Create new user
            const newUser = {
                id: db.users.length + 1,
                email: body.email,
                password: body.password,
                name: body.name,
                token: `token-${Date.now()}-${Math.random()}`
            };

            db.users.push(newUser);

            const { password, ...userData } = newUser;
            sendJSON(res, 201, { user: userData });
        });
        return;
    }

    if (path === '/api/auth/me' && method === 'GET') {
        const user = getAuthUser(req);

        if (user) {
            const { password, ...userData } = user;
            sendJSON(res, 200, { user: userData });
        } else {
            sendJSON(res, 401, { error: 'Unauthorized' });
        }
        return;
    }

    if (path === '/api/orders' && method === 'POST') {
        const user = getAuthUser(req);

        if (!user) {
            sendJSON(res, 401, { error: 'Unauthorized' });
            return;
        }

        parseBody(req, (err, body) => {
            if (err) {
                sendJSON(res, 400, { error: 'Invalid JSON' });
                return;
            }

            const order = {
                id: db.orders.length + 1,
                userId: user.id,
                items: body.items,
                shippingAddress: body.shippingAddress,
                total: body.items.reduce((sum, item) => sum + (item.price * item.quantity), 0),
                status: 'pending',
                createdAt: new Date().toISOString()
            };

            db.orders.push(order);
            sendJSON(res, 201, { order });
        });
        return;
    }

    if (path === '/api/orders' && method === 'GET') {
        const user = getAuthUser(req);

        if (!user) {
            sendJSON(res, 401, { error: 'Unauthorized' });
            return;
        }

        const orders = db.orders.filter(o => o.userId === user.id);
        sendJSON(res, 200, { orders });
        return;
    }

    // 404
    sendJSON(res, 404, { error: 'Not found' });
}

// Start server
const server = http.createServer(handleRequest);

server.listen(PORT, () => {
    console.log('🛒 OpenFlex E-Commerce Mock API Server');
    console.log(`✓ Server running at http://localhost:${PORT}`);
    console.log('\nAvailable endpoints:');
    console.log('  GET  /api/products');
    console.log('  GET  /api/products?category=Electronics');
    console.log('  GET  /api/products/:id');
    console.log('  GET  /api/products/search?q=query');
    console.log('  POST /api/auth/login');
    console.log('  POST /api/auth/register');
    console.log('  GET  /api/auth/me');
    console.log('  POST /api/orders');
    console.log('  GET  /api/orders');
    console.log('\nDemo credentials:');
    console.log('  Email: demo@openflex.org');
    console.log('  Password: demo123');
    console.log('\nPress Ctrl+C to stop\n');
});
