<template>
    <div id="app">
        <div>
            <b-navbar toggleable="lg" type="dark" variant="dark">
                <b-navbar-brand href="#">DoIT!</b-navbar-brand>

                <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

                <b-collapse id="nav-collapse" is-nav>
                    <b-navbar-nav>
                        <b-nav-item>
                            <router-link to="/login" class="active" style="color: white;">Login</router-link>
                        </b-nav-item>
                        <b-nav-item>
                            <router-link to="/register" style="color: white;">Register</router-link>
                        </b-nav-item>
                    </b-navbar-nav>
                </b-collapse>
            </b-navbar>
        </div>
        <hr>
        <div>
            <router-view />
        </div>
        
    </div>
</template>
