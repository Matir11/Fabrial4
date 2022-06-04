<template>
  <div class="home">
    <h1 class="title">Fabrial</h1>

    <hr>

    <div class="columns">
      <div class="column is-3 is-offset-3">
        <form v-on:submit.prevent="addTask">

          <h2 class="subtitle">Add Task</h2>

          <div class="field">
            <label class="label">Description</label>
            <div class="control">
              <input class="input" type="text" v-model="description">
            </div>
          </div>

          <div class="field">
            <label class="label">Price</label>
            <div class="control">
              <input class="input" type="text" v-model="chore_value">
            </div>
          </div>

           <div class="field">
            <label class="label">Status</label>
            <div class="control">
              <div class="select">
                <select v-model="status">
                  <option value="todo">To Do</option>
                  <option value="done">Done</option>
                </select>
              </div>
            </div>
          </div>

          <div class="field">
            <div class="control">
              <button class="button is-link">Submit</button>
            </div>
          </div>

        </form>
      </div>
    </div>
    <div class="columns">

      <div class="column is-6">
        <h2 class="subtitle">To Do</h2>
        <div class="todo">
          <div class="card" v-for="task in tasks" v-if="task.status ==='todo'" v-bind:key="task.id" >
            <div class="card-content">{{ task.description }}</div>

            <footer class="card-footer">
              <a class="card-footer-item">Done</a>
            </footer>
          </div>
        </div>
      </div>

      <div class="column is-6">
        <h2 class="subtitle">Done</h2>
        <div class="done">
          <div class="card" v-for="task in tasks" v-if="task.status ==='done'" v-bind:key="task.id" >
            <div class="card-content">{{ task.description }}</div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Home',
  data () {
    return {
      tasks: [],
      description: '',
      chore_value: '',
      status: 'todo'
    }
  },
  mounted () {
    this.getTasks()
  },
  methods: {
    getTasks() {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/tasks/',
        auth: {
          username: 'architect',
          password: 'This,ISfun',
        }
      }).then(response => this.tasks = response.data)
    },
    addTask() {
      if (this.description) {
        axios({
          method: 'post',
        url: 'http://127.0.0.1:8000/tasks/',
        data: {
          description: this.description,
          chore_value: this.chore_value,
          status: this.status,
        },
        auth: {
          username: 'architect',
          password: 'This,ISfun',
        }
        }).then((response) => {
          let newTask = {
            'id': response.data.id,
            'description': this.description,
            'chore_value': this.chore_value,
            'status': this.status,
          }

          this.tasks.push(newTask)

          this.description = ''
          this.chore_value = ''
          this.status = ''
        }).catch((error) => {
          console.log(error)
        })
      }
    }
  }
}
</script>

<style lang="scss">
.select, select {
  width: 100%;
}

.card {
  margin-bottom: 20px;
}

.done {
  opacity: 0.3;
}
</style>