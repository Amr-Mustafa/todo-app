<template>
    <div id="app">
        <h1>
            Vuejs Todo app
        </h1>

        <div>
            <router-link to="/login">Login</router-link>
            <router-link to="/register">Register</router-link>
        </div>

        <div>
            <router-view />
        </div>
        
    </div>
</template>

<style>
#app {
  margin-top: 60px
}
</style>
