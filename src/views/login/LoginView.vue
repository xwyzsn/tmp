<template>
<div >
    <div class="tw-fixed tw-inset-0 tw-flex tw-items-center tw-justify-center">
        <div class="tw-border tw-border-gray-200 tw-shadow">
            <el-form class="tw-m-3 tw-p-3" :model="form" label-width="120px">
            <el-form-item label="username">
              <el-input v-model="form.name" />
            </el-form-item>
            <el-form-item label="password">
                <el-input v-model="form.password" />
            </el-form-item>
            <el-form-item class="tw-grid tw-grid-cols-2 tw-gap-10 ">
                <el-button type="primary">登陆</el-button>
                <el-button type="default">取消</el-button>
            </el-form-item>
            </el-form>
        </div>
    </div>
</div>
</template>

<script setup>
import {ref} from 'vue'

let form = ref({
    name:'',
    password:''
})

</script>