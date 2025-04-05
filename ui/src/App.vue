<template>
  <div id="app">

    <!-- Navbar Section -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">
          <div class="d-flex flex-column ms-4">
        <h1 class="fs-1 fw-bold mb-0">Crypto</h1>
        <div class="ms-2">
          <!-- <h6 class="mb-0">Currency</h6> -->
          <h6 class="mb-0">Dashboard</h6>
        </div>
      </div>
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link to="/" class="nav-link" active-class="active">Home Page</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/dashboard" class="nav-link" active-class="active">Dashboard</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <main class="container mt-5 flex-grow-1">
      <router-view></router-view>
    </main>
    <footer class="bg-dark text-white text-center py-3">
      <p>&copy; 2025 Crypto Dashboard. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
body {
  background-color: #f2f9fb !important; 
  margin: 0;
  font-family: Arial, sans-serif;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}


.header {
  background-color: #0073b4;
  color: white;
  text-align: center;
  padding: 20px 0;
}


footer {
  background-color: #35495e; 
  color: white;
  text-align: center;
  padding: 10px 0;
}

main {
  padding: 20px;
  flex-grow: 1;
}

</style>