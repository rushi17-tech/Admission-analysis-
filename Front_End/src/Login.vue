<template>
    <div>
        <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="email">Email</label>
        <input id="email" type="text" v-model="email" class="form-control" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input id="password" type="password" v-model="password" class="form-control" />
      </div>

            <div class="my-3">
                <button type="submit" class="btn btn-primary">
                    Login
                </button>

            </div>
        </form>
    </div>
</template>
<script setup>

</script>   