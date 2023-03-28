<template>
    <div class="tw-w-full tw-h-full">
        <el-row class="tw-mt-10">
            <el-button type="primary" @click="dialogVisible = true">添加</el-button>
            <el-button type="error" @click="deleteRow">删除</el-button>
        </el-row>
        <el-dialog v-model="dialogVisible" title="添加食物" width="50%" :before-close="handleClose">
            <div>
                <el-form>
                    <el-form-item label="名称">
                        <el-input v-model="form.name"></el-input>
                    </el-form-item>
                    <el-form-item label="图片">
                        <el-input v-model="form.image"></el-input>
                    </el-form-item>
                    <el-form-item label="价格">
                        <el-input v-model="form.price"></el-input>
                    </el-form-item>
                    <el-form-item label="描述">
                        <el-input v-model="form.description"></el-input>
                    </el-form-item>
                    <el-form-item label="评分">
                        <el-input v-model="form.rating"></el-input>
                    </el-form-item>
                    <el-form-item label="用时">
                        <el-input v-model="form.time"></el-input>
                    </el-form-item>
                    <el-form-item label="类别">
                        <el-input v-model="form.category"></el-input>
                    </el-form-item>
                </el-form>

            </div>
            <template #footer>
                <span class="dialog-footer">
                    <el-button @click="dialogVisible = false">Cancel</el-button>
                    <el-button type="primary" @click="addNew">
                        Confirm
                    </el-button>
                </span>
            </template>
        </el-dialog>

        <el-table ref="singleTableRef" highlight-current-row @current-change="handleCurrentChange" v-if="tableData"
            :data="tableData" class="tw-mt-5 tw-w-full tw-h-full">
            <el-table-column prop="id" label="id" class="tw-w-1/2"></el-table-column>
            <el-table-column prop="name" label="名称" width="180"></el-table-column>
            <el-table-column prop="image" label="图片" width="180">
                <template #default="{ row }">
                    <img :src="row.image" alt="" class="tw-w-1/2 tw-h-1/2">
                </template>
            </el-table-column>
            <el-table-column prop="price" label="价格" width="180"></el-table-column>
            <el-table-column prop="description" label="描述" width="180"></el-table-column>
            <el-table-column prop="rating" label="评分" width="180"></el-table-column>
            <el-table-column prop="time" label="用时" width="180"></el-table-column>

            <el-table-column prop="category" label="类别" width="180"></el-table-column>
            <!-- <el-table-column prop="ingredients" label="原料" width="180"></el-table-column> -->
        </el-table>

    </div>
</template>
 
<script setup>
import { api } from '../../boot/api';
import { ref } from 'vue';
import { ElMessage } from 'element-plus';
let tableData = ref([])
api('/getfood', { method: 'GET' }).then((res) => {
    tableData.value = res.data;
    console.log(tableData.value)
})
let dialogVisible = ref(false)
let form = ref({
    name: '',
    image: '',
    price: '',
    description: '',
    rating: '',
    time: '',
    category: ''
})
let singleTableRef = ref()
const currentRow = ref()

const addNew = ()=>{
    api('/addfood', { method: 'POST',data:form.value }).then((res) => {
        api('/getfood', { method: 'GET' }).then((res) => {
            tableData.value = res.data;
            console.log(tableData.value)
            form.value = {
                name: '',
                image: '',
                price: '',
                description: '',
                rating: '',
                time: '',
                category: ''
            }
            dialogVisible.value = false
            ElMessage({
                message: '添加成功',
                type: 'success'
            });
        })
    })
}

const setCurrent = (row) => {
    singleTableRef.value.setCurrentRow(row)
}
const handleCurrentChange = (val) => {
    currentRow.value = val
    console.log(val)
}
const deleteRow = () => {
    if (currentRow.value) {
        let id = currentRow.value.id
        api('/deletefood', { method: 'GET',params:{fid:id} }).then((res) => {
            api('/getfood', { method: 'GET' }).then((res) => {
                tableData.value = res.data;
                ElMessage({
                message: '删除成功',
                type: 'success'
            });
            })
        })
    }
}
</script> 
 
<style scoped></style>
