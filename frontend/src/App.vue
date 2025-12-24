<template>
  <div class="page">
    <h1 style="color:blue;">Welcome to Tasks!</h1>

    <!-- TABLE -->
    <h2>Tasks</h2>
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Title</th>
          <th>Description</th>
          <th>Status</th>
          <th>Created</th>
          <th>Modified</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(task, loc) in tasks_list" :key="loc">
          <td>{{ loc }}</td>
          <td>{{ task.title }}</td>
          <td>{{ task.description }}</td>
          <td>{{ task.status }}</td>
          <td>{{ task.created_at }}</td>
          <td>{{ task.updated_at }}</td>
          <td>
            <button @click="startEdit(loc, task)">Edit</button>
            <button v-if="task.status !== 'open'"        @click="patchStatus(loc, 'open')">open</button>
            <button v-if="task.status !== 'in_progress'" @click="patchStatus(loc, 'in_progress')">in_progress</button>
            <button v-if="task.status !== 'done'"        @click="patchStatus(loc, 'done')">done</button>     
            <button @click="deleteTask(loc)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h2>Create Task</h2>

    <!-- FORM -->
    <form @submit.prevent="createTask" class="form">
      <input v-model="title" placeholder="Title" required />
      <input v-model="description" placeholder="Description (optional)" />
      <input v-model="status" placeholder="Status (default: open)" />
      <button type="submit">Add</button>
    </form>

    <h2>Edit Task</h2>

    <form @submit.prevent="submitUpdate" class="form">
      <input v-model="editTitle" placeholder="Title" required />
      <input v-model="editDescription" placeholder="Description (optional)" />
      <input v-model="editStatus" placeholder="Status (open/in_progress/done)" />
      <button type="submit">Update</button>
      <button type="button" @click="cancelEdit">Cancel</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      title: "",
      description: "",
      status: "",
      tasks_list: {},

      // edit form state
      editingLoc: null,
      editTitle: "",
      editDescription: "",
      editStatus: ""
    };
  },
  async mounted() {
      await this.loadTasks();
},
  methods: {
    async loadTasks() {
      const res = await axios.get("/api/tasks", {
        headers: { "Cache-Control": "no-cache" }
      });

      const locations = res.data

      const promises = locations.map(loc =>
        axios.get(`/api/${loc}`, {
          headers: { "Cache-Control": "no-cache" }
        })
      );
      
      const responses = await Promise.all(promises);
      
      this.tasks_list = {};
      responses.forEach((r, i) => {
        const loc = locations[i];
        this.tasks_list[loc] = r.data;
      });
    },
    async createTask() {
      const payload = { title: this.title };

      if (this.description.trim() !== "") {
        payload.description = this.description;
      }      
      if (this.status.trim() !== "") {
        payload.status = this.status;
      }
      await axios.post("/api/tasks", payload,
      
      {
        headers: { "Cache-Control": "no-cache" }
      });
      
      this.title = "";
      this.description = "";
      this.status = "";  

      await this.loadTasks();
    },

    startEdit(loc, task) {
      this.editingLoc = loc;
      this.editTitle = task.title ?? "";
      this.editDescription = task.description ?? "";
      this.editStatus = task.status ?? "";
    },
  
    cancelEdit() {
      this.editingLoc = null;
      this.editTitle = "";
      this.editDescription = "";
      this.editStatus = "";
    },
  
    async submitUpdate() {
      const payload = { title: this.editTitle };
  
      if (this.editDescription.trim() !== "") payload.description = this.editDescription;
      if (this.editStatus.trim() !== "") payload.status = this.editStatus;
  
      await axios.put(`/api/${this.editingLoc}`, payload, {
        headers: { "Cache-Control": "no-cache" }
      });
  
      await this.loadTasks();
      this.cancelEdit();
    },

    async deleteTask(loc) {
      await axios.delete(`/api/${loc}`);

      await this.loadTasks();
    },

    async patchStatus(loc, status) {
      await axios.patch(`/api/${loc}`, status);

      await this.loadTasks();
    }
  }
};
</script>


<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
