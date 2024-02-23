import { createRouter, createWebHistory } from 'vue-router'
import { useAuth } from '../store/auth'
import Home from '../views/Home.vue'

const authGuard = (to, from, next) => {
    const { getAuthData } = useAuth()
    if (to.name !== 'Login' && to.name !== 'Register' && !getAuthData) {
        next({ name: 'Login' })
    } else {
        next()
    }
}

const adminAuthGuard = (to, from, next) => {
    const { getAuthData } = useAuth()
    next()
    if (getAuthData && getAuthData.is_admin) {
        next()
    } else {
        next({ name: 'Home' })
    }
}

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    // nested admin routes
    {
        path: '/admin',
        name: 'Admin',
        beforeEnter: adminAuthGuard,
        children: [
            {
                path: '',
                name: 'Admin',
                component: () => import('../views/admin/AdminHome.vue')
            },
            {
                path: 'groups',
                name: 'AdminGroups',
                component: () => import('../views/admin/AdminGroup.vue')
            },
            {
                path: 'users',
                name: 'AdminUsers',
                component: () => import('../views/admin/AdminUser.vue')
            },
        ]
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('../views/Login.vue')
    },
    {
        path: '/register',
        name: 'Register',
        component: () => import('../views/Register.vue')
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue')
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach(authGuard)

export default router
