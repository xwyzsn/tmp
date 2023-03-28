<template>
      <el-container class="tw-w-full tw-h-full">
        <el-header style="background-color:rgb(36, 49, 68)" class="tw-text-white tw-text-3xl">
          点餐系统后台
        </el-header>
        <el-container class="tw-w-full tw-h-full">
          <el-aside 
          style="background-color:rgb(36, 49, 68)"
          width="200px" >
            <el-menu
          default-active="0"
          router
          style="background-color:rgb(36, 49, 68)"
          class="el-menu-vertical-demo tw-text-white"
          @open="handleOpen"
          @close="handleClose"
           >
          <el-menu-item class="tw-text-white hover:tw-text-black" route="/home/index" index="0">首页</el-menu-item>
          <el-menu-item class="tw-text-white hover:tw-text-black" route="/home/order" index="1">点菜页</el-menu-item>
          <el-menu-item class="tw-text-white hover:tw-text-black" route="/home/food" index="1">食物页</el-menu-item>
          <el-menu-item class="tw-text-white hover:tw-text-black" route="/home/history" index="1">历史订单</el-menu-item>


        </el-menu>
          </el-aside>
          <el-main class="">
            <RouterView></RouterView>
          </el-main>
        </el-container>
      </el-container>
  </template>
  
<script setup>
import { ref,onMounted } from 'vue'
const handleOpen = (key, keyPath) => {
  console.log(key, keyPath)
}
const handleClose = (key, keyPath) => {
  console.log(key, keyPath)
}

</script>
