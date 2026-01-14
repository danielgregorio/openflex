/**
 * OpenFlex CMS - Mock API Server
 *
 * A simple Express.js server providing mock REST API for CMS development
 *
 * Usage:
 *   node mock-api-server.js
 *
 * Endpoints:
 *   POST   /api/auth/login         - Login
 *   POST   /api/auth/logout        - Logout
 *   GET    /api/auth/me            - Get current user
 *   GET    /api/posts              - List posts (with filters)
 *   GET    /api/posts/:id          - Get single post
 *   POST   /api/posts              - Create post
 *   PUT    /api/posts/:id          - Update post
 *   DELETE /api/posts/:id          - Delete post
 *   POST   /api/posts/:id/publish  - Publish post
 *   GET    /api/media              - List media files
 *   POST   /api/media/upload       - Upload media file
 *   DELETE /api/media/:id          - Delete media file
 *   GET    /api/users              - List users
 *   POST   /api/users              - Create user
 *   PUT    /api/users/:id          - Update user
 *   DELETE /api/users/:id          - Delete user
 *   GET    /api/analytics          - Get analytics data
 */

const express = require('express');
const cors = require('cors');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use('/uploads', express.static('uploads'));

// Multer configuration for file uploads
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        const uploadDir = './uploads';
        if (!fs.existsSync(uploadDir)) {
            fs.mkdirSync(uploadDir);
        }
        cb(null, uploadDir);
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, uniqueSuffix + path.extname(file.originalname));
    }
});
const upload = multer({ storage, limits: { fileSize: 10 * 1024 * 1024 } }); // 10MB limit

// In-memory database
let db = {
    users: [
        {
            id: 1,
            email: 'admin@openflex.org',
            name: 'Admin User',
            password: 'admin123',
            role: 'Admin',
            avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Admin',
            token: 'admin-token-12345',
            createdAt: '2024-01-01T00:00:00Z'
        },
        {
            id: 2,
            email: 'editor@openflex.org',
            name: 'Jane Editor',
            password: 'editor123',
            role: 'Editor',
            avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jane',
            token: 'editor-token-67890',
            createdAt: '2024-01-15T00:00:00Z'
        },
        {
            id: 3,
            email: 'author@openflex.org',
            name: 'John Author',
            password: 'author123',
            role: 'Author',
            avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John',
            token: 'author-token-11111',
            createdAt: '2024-02-01T00:00:00Z'
        }
    ],

    posts: [
        {
            id: 1,
            title: 'Welcome to OpenFlex CMS',
            slug: 'welcome-to-openflex-cms',
            body: '# Welcome to OpenFlex CMS\n\nThis is a modern content management system built with **OpenFlex Neo**.\n\n## Features\n\n- Reactive state management\n- WYSIWYG editor\n- Media library\n- User management\n- Analytics dashboard\n\n```javascript\nconst cms = new CMSState();\nconst post = await cms.createPost({\n  title: "My Post",\n  body: "Content here..."\n});\n```\n\nEnjoy building with OpenFlex! 🚀',
            excerpt: 'A modern content management system built with OpenFlex Neo',
            featuredImage: 'https://picsum.photos/800/400?random=1',
            authorId: 1,
            categories: ['Tutorial', 'Getting Started'],
            tags: ['cms', 'openflex', 'tutorial'],
            status: 'Published',
            viewCount: 245,
            publishedAt: '2024-01-10T10:00:00Z',
            createdAt: '2024-01-09T15:00:00Z',
            updatedAt: '2024-01-10T10:00:00Z'
        },
        {
            id: 2,
            title: 'Building Modern Web Applications',
            slug: 'building-modern-web-applications',
            body: '# Building Modern Web Applications\n\nLearn how to build scalable web applications using reactive programming patterns.\n\n## Key Concepts\n\n- Component-based architecture\n- State management with signals\n- Async/await for data fetching\n- Type-safe development\n\n> "The best code is the code that doesn\'t need to be written." - Anonymous\n\nStart building today!',
            excerpt: 'Learn how to build scalable web applications using reactive programming',
            featuredImage: 'https://picsum.photos/800/400?random=2',
            authorId: 2,
            categories: ['Development', 'Tutorial'],
            tags: ['web development', 'javascript', 'reactive'],
            status: 'Published',
            viewCount: 189,
            publishedAt: '2024-01-15T14:30:00Z',
            createdAt: '2024-01-14T09:00:00Z',
            updatedAt: '2024-01-15T14:30:00Z'
        },
        {
            id: 3,
            title: 'Migrating from Flash to OpenFlex',
            slug: 'migrating-from-flash-to-openflex',
            body: '# Migrating from Flash to OpenFlex\n\nStep-by-step guide to migrate your Flash applications to OpenFlex Neo.\n\n## Migration Steps\n\n1. Analyze your ActionScript code\n2. Convert to AS4 syntax\n3. Update MXML components\n4. Test and deploy\n\n## Benefits\n\n- Modern JavaScript output\n- Better performance\n- Type safety\n- Active development',
            excerpt: 'Step-by-step guide to migrate Flash applications to OpenFlex Neo',
            featuredImage: 'https://picsum.photos/800/400?random=3',
            authorId: 1,
            categories: ['Migration', 'Guide'],
            tags: ['flash', 'migration', 'legacy'],
            status: 'Published',
            viewCount: 412,
            publishedAt: '2024-01-20T11:00:00Z',
            createdAt: '2024-01-18T16:00:00Z',
            updatedAt: '2024-01-20T11:00:00Z'
        },
        {
            id: 4,
            title: 'Understanding Reactive Programming',
            slug: 'understanding-reactive-programming',
            body: '# Understanding Reactive Programming\n\nDraft article about reactive programming concepts...\n\nTODO:\n- Add code examples\n- Explain @reactive decorator\n- Show computed properties\n- Add diagrams',
            excerpt: 'Learn the fundamentals of reactive programming',
            featuredImage: '',
            authorId: 3,
            categories: ['Tutorial'],
            tags: ['reactive', 'programming'],
            status: 'Draft',
            viewCount: 0,
            publishedAt: null,
            createdAt: '2024-01-25T08:00:00Z',
            updatedAt: '2024-01-25T12:00:00Z'
        },
        {
            id: 5,
            title: 'Performance Optimization Tips',
            slug: 'performance-optimization-tips',
            body: '# Performance Optimization Tips\n\n## Bundle Size Optimization\n\n- Tree shaking removes unused code\n- Minification reduces file size\n- Code splitting improves load times\n\n## Runtime Performance\n\n- Use computed properties wisely\n- Avoid unnecessary reactivity\n- Optimize re-renders\n- Profile with browser DevTools',
            excerpt: 'Tips and tricks for optimizing OpenFlex applications',
            featuredImage: 'https://picsum.photos/800/400?random=4',
            authorId: 2,
            categories: ['Performance', 'Best Practices'],
            tags: ['optimization', 'performance', 'tips'],
            status: 'Draft',
            viewCount: 0,
            publishedAt: null,
            createdAt: '2024-01-28T10:00:00Z',
            updatedAt: '2024-01-29T14:00:00Z'
        }
    ],

    media: [
        {
            id: 1,
            filename: 'hero-image.jpg',
            url: 'https://picsum.photos/1200/600?random=10',
            thumbnailUrl: 'https://picsum.photos/300/200?random=10',
            mimeType: 'image/jpeg',
            size: 245632,
            width: 1200,
            height: 600,
            uploadedBy: 1,
            uploadedAt: '2024-01-05T09:00:00Z',
            alt: 'Hero image',
            caption: 'Beautiful landscape'
        },
        {
            id: 2,
            filename: 'screenshot.png',
            url: 'https://picsum.photos/1000/700?random=11',
            thumbnailUrl: 'https://picsum.photos/300/200?random=11',
            mimeType: 'image/png',
            size: 512000,
            width: 1000,
            height: 700,
            uploadedBy: 1,
            uploadedAt: '2024-01-08T11:30:00Z',
            alt: 'Application screenshot',
            caption: 'Dashboard view'
        },
        {
            id: 3,
            filename: 'diagram.svg',
            url: '/uploads/diagram.svg',
            thumbnailUrl: '/uploads/diagram.svg',
            mimeType: 'image/svg+xml',
            size: 8192,
            width: 800,
            height: 600,
            uploadedBy: 2,
            uploadedAt: '2024-01-12T14:00:00Z',
            alt: 'Architecture diagram',
            caption: 'System architecture'
        },
        {
            id: 4,
            filename: 'presentation.pdf',
            url: '/uploads/presentation.pdf',
            thumbnailUrl: '/uploads/pdf-icon.png',
            mimeType: 'application/pdf',
            size: 1024000,
            width: 0,
            height: 0,
            uploadedBy: 2,
            uploadedAt: '2024-01-15T16:45:00Z',
            alt: 'Presentation slides',
            caption: 'Conference presentation'
        }
    ],

    analytics: {
        totalPosts: 5,
        totalPages: 0,
        totalMedia: 4,
        totalViews: 846,
        totalComments: 23,
        viewsToday: 47,
        viewsThisWeek: 156,
        viewsThisMonth: 423,
        topPosts: [1, 3, 2], // Post IDs
        recentActivity: [
            { type: 'post_created', userId: 3, postId: 5, timestamp: '2024-01-28T10:00:00Z' },
            { type: 'post_updated', userId: 2, postId: 5, timestamp: '2024-01-29T14:00:00Z' },
            { type: 'media_uploaded', userId: 2, mediaId: 4, timestamp: '2024-01-15T16:45:00Z' }
        ]
    }
};

// Helper functions
function findUserByToken(token) {
    if (!token) return null;
    const tokenValue = token.replace('Bearer ', '');
    return db.users.find(u => u.token === tokenValue);
}

function requireAuth(req, res, next) {
    const user = findUserByToken(req.headers.authorization);
    if (!user) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    req.user = user;
    next();
}

function getUserFromPost(post) {
    return db.users.find(u => u.id === post.authorId);
}

// ============================================================================
// AUTH ENDPOINTS
// ============================================================================

app.post('/api/auth/login', (req, res) => {
    const { email, password } = req.body;
    const user = db.users.find(u => u.email === email && u.password === password);

    if (!user) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }

    const { password: _, ...userWithoutPassword } = user;

    res.json({
        user: userWithoutPassword,
        token: user.token
    });
});

app.post('/api/auth/logout', requireAuth, (req, res) => {
    res.json({ message: 'Logged out successfully' });
});

app.get('/api/auth/me', requireAuth, (req, res) => {
    const { password: _, ...userWithoutPassword } = req.user;
    res.json({ user: userWithoutPassword });
});

// ============================================================================
// POSTS ENDPOINTS
// ============================================================================

app.get('/api/posts', (req, res) => {
    let posts = [...db.posts];

    // Filter by status
    if (req.query.status) {
        posts = posts.filter(p => p.status.toLowerCase() === req.query.status.toLowerCase());
    }

    // Filter by category
    if (req.query.category) {
        posts = posts.filter(p => p.categories.includes(req.query.category));
    }

    // Filter by author
    if (req.query.author) {
        posts = posts.filter(p => p.authorId === parseInt(req.query.author));
    }

    // Search
    if (req.query.q) {
        const query = req.query.q.toLowerCase();
        posts = posts.filter(p =>
            p.title.toLowerCase().includes(query) ||
            p.body.toLowerCase().includes(query) ||
            p.excerpt.toLowerCase().includes(query)
        );
    }

    // Add author data
    const postsWithAuthors = posts.map(post => ({
        ...post,
        author: getUserFromPost(post)
    }));

    res.json({ posts: postsWithAuthors });
});

app.get('/api/posts/:id', (req, res) => {
    const post = db.posts.find(p => p.id === parseInt(req.params.id));

    if (!post) {
        return res.status(404).json({ error: 'Post not found' });
    }

    const postWithAuthor = {
        ...post,
        author: getUserFromPost(post)
    };

    res.json({ post: postWithAuthor });
});

app.post('/api/posts', requireAuth, (req, res) => {
    const newPost = {
        id: Math.max(...db.posts.map(p => p.id), 0) + 1,
        ...req.body,
        authorId: req.user.id,
        viewCount: 0,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
    };

    db.posts.push(newPost);

    const postWithAuthor = {
        ...newPost,
        author: getUserFromPost(newPost)
    };

    res.status(201).json({ post: postWithAuthor });
});

app.put('/api/posts/:id', requireAuth, (req, res) => {
    const index = db.posts.findIndex(p => p.id === parseInt(req.params.id));

    if (index === -1) {
        return res.status(404).json({ error: 'Post not found' });
    }

    db.posts[index] = {
        ...db.posts[index],
        ...req.body,
        id: db.posts[index].id, // Preserve ID
        authorId: db.posts[index].authorId, // Preserve author
        viewCount: db.posts[index].viewCount, // Preserve view count
        createdAt: db.posts[index].createdAt, // Preserve creation date
        updatedAt: new Date().toISOString()
    };

    const postWithAuthor = {
        ...db.posts[index],
        author: getUserFromPost(db.posts[index])
    };

    res.json({ post: postWithAuthor });
});

app.delete('/api/posts/:id', requireAuth, (req, res) => {
    const index = db.posts.findIndex(p => p.id === parseInt(req.params.id));

    if (index === -1) {
        return res.status(404).json({ error: 'Post not found' });
    }

    db.posts.splice(index, 1);
    res.json({ message: 'Post deleted' });
});

app.post('/api/posts/:id/publish', requireAuth, (req, res) => {
    const post = db.posts.find(p => p.id === parseInt(req.params.id));

    if (!post) {
        return res.status(404).json({ error: 'Post not found' });
    }

    post.status = 'Published';
    post.publishedAt = new Date().toISOString();
    post.updatedAt = new Date().toISOString();

    const postWithAuthor = {
        ...post,
        author: getUserFromPost(post)
    };

    res.json({ post: postWithAuthor });
});

// ============================================================================
// MEDIA ENDPOINTS
// ============================================================================

app.get('/api/media', (req, res) => {
    let media = [...db.media];

    // Filter by type
    if (req.query.type) {
        media = media.filter(m => m.mimeType.startsWith(req.query.type));
    }

    // Search
    if (req.query.q) {
        const query = req.query.q.toLowerCase();
        media = media.filter(m =>
            m.filename.toLowerCase().includes(query) ||
            m.alt.toLowerCase().includes(query)
        );
    }

    res.json({ media });
});

app.post('/api/media/upload', requireAuth, upload.single('file'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    const newMedia = {
        id: Math.max(...db.media.map(m => m.id), 0) + 1,
        filename: req.file.originalname,
        url: `/uploads/${req.file.filename}`,
        thumbnailUrl: `/uploads/${req.file.filename}`,
        mimeType: req.file.mimetype,
        size: req.file.size,
        width: 0, // Would need image processing library for real dimensions
        height: 0,
        uploadedBy: req.user.id,
        uploadedAt: new Date().toISOString(),
        alt: req.body.alt || '',
        caption: req.body.caption || ''
    };

    db.media.push(newMedia);
    res.status(201).json({ media: newMedia });
});

app.delete('/api/media/:id', requireAuth, (req, res) => {
    const index = db.media.findIndex(m => m.id === parseInt(req.params.id));

    if (index === -1) {
        return res.status(404).json({ error: 'Media not found' });
    }

    // Delete file from disk
    const media = db.media[index];
    if (media.url.startsWith('/uploads/')) {
        const filepath = path.join(__dirname, media.url);
        if (fs.existsSync(filepath)) {
            fs.unlinkSync(filepath);
        }
    }

    db.media.splice(index, 1);
    res.json({ message: 'Media deleted' });
});

// ============================================================================
// USERS ENDPOINTS
// ============================================================================

app.get('/api/users', requireAuth, (req, res) => {
    const users = db.users.map(({ password, token, ...user }) => user);
    res.json({ users });
});

app.post('/api/users', requireAuth, (req, res) => {
    // Only admins can create users
    if (req.user.role !== 'Admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }

    const newUser = {
        id: Math.max(...db.users.map(u => u.id), 0) + 1,
        ...req.body,
        token: `token-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        createdAt: new Date().toISOString()
    };

    db.users.push(newUser);

    const { password, token, ...userWithoutSensitive } = newUser;
    res.status(201).json({ user: userWithoutSensitive });
});

app.put('/api/users/:id', requireAuth, (req, res) => {
    const index = db.users.findIndex(u => u.id === parseInt(req.params.id));

    if (index === -1) {
        return res.status(404).json({ error: 'User not found' });
    }

    // Only admins or the user themselves can update
    if (req.user.role !== 'Admin' && req.user.id !== parseInt(req.params.id)) {
        return res.status(403).json({ error: 'Forbidden' });
    }

    db.users[index] = {
        ...db.users[index],
        ...req.body,
        id: db.users[index].id, // Preserve ID
        token: db.users[index].token, // Preserve token
        createdAt: db.users[index].createdAt // Preserve creation date
    };

    const { password, token, ...userWithoutSensitive } = db.users[index];
    res.json({ user: userWithoutSensitive });
});

app.delete('/api/users/:id', requireAuth, (req, res) => {
    // Only admins can delete users
    if (req.user.role !== 'Admin') {
        return res.status(403).json({ error: 'Forbidden' });
    }

    const index = db.users.findIndex(u => u.id === parseInt(req.params.id));

    if (index === -1) {
        return res.status(404).json({ error: 'User not found' });
    }

    db.users.splice(index, 1);
    res.json({ message: 'User deleted' });
});

// ============================================================================
// ANALYTICS ENDPOINTS
// ============================================================================

app.get('/api/analytics', requireAuth, (req, res) => {
    // Populate top posts with full data
    const topPosts = db.analytics.topPosts
        .map(id => db.posts.find(p => p.id === id))
        .filter(Boolean)
        .map(post => ({
            ...post,
            author: getUserFromPost(post)
        }));

    res.json({
        ...db.analytics,
        topPosts
    });
});

// ============================================================================
// START SERVER
// ============================================================================

app.listen(PORT, () => {
    console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║           OpenFlex CMS - Mock API Server Running             ║
║                                                               ║
║  Server:  http://localhost:${PORT}                                 ║
║  API:     http://localhost:${PORT}/api                             ║
║                                                               ║
║  Demo Accounts:                                               ║
║  ┌─────────────────────────────────────────────────────────┐ ║
║  │ Admin:       admin@openflex.org / admin123              │ ║
║  │ Editor:      editor@openflex.org / editor123            │ ║
║  │ Author:      author@openflex.org / author123            │ ║
║  └─────────────────────────────────────────────────────────┘ ║
║                                                               ║
║  Endpoints: ${Object.keys(app._router.stack.filter(r => r.route).length)} routes available                                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    `);
});
