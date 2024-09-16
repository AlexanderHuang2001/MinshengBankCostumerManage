new Vue({
    el: '#app',
    data: {
        filters: {
            ip: '',
            userId: '',
            phone: '',
            marketingLimit: '',
            greetingLimit: '',
            riskLimit: '',
            provinceFilter: '',
            selectedProvinces: []
        },
        provinces: ['北京', '上海', '天津', '重庆', '广东', '浙江', '江苏', '福建', '山东', '四川', '湖南', '湖北', '河北', '河南', '安徽', '江西', '山西', '陕西', '辽宁', '吉林', '黑龙江', '广西', '云南', '贵州', '海南', '内蒙古', '宁夏', '青海', '新疆', '西藏', '甘肃'],
        selectAll: false,
        selectedRows: [],
        currentPage: 1,
        itemsPerPage: 10,
        data: []  // 初始数据为空
    },
    computed: {
        filteredData() {
            return this.data.filter(item => {
                return (!this.filters.ip || item.ip.includes(this.filters.ip)) &&
                    (!this.filters.userId || item.id.toString().includes(this.filters.userId)) &&
                    (!this.filters.phone || item.phone.includes(this.filters.phone)) &&
                    (!this.filters.marketingLimit || item.marketingLimit <= this.filters.marketingLimit) &&
                    (!this.filters.greetingLimit || item.greetingLimit >= this.filters.greetingLimit) &&
                    (!this.filters.riskLimit || item.riskLimit <= this.filters.riskLimit) &&
                    (this.filters.provinceFilter !== 'include' || this.filters.selectedProvinces.includes(item.province)) &&
                    (this.filters.provinceFilter !== 'exclude' || !this.filters.selectedProvinces.includes(item.province));
            });
        },
        paginatedData() {
            return this.filteredData.slice((this.currentPage - 1) * this.itemsPerPage, this.itemsPerPage * this.currentPage);
        },
        startIndex() {
            return (this.currentPage - 1) * this.itemsPerPage;
        },
        endIndex() {
            return Math.min(this.startIndex + this.itemsPerPage, this.filteredData.length);
        }
    },
    watch: {
        selectAll(newValue) {
            this.selectedRows = newValue ? this.paginatedData.map(item => item.id) : [];
        }
    },
    methods: {
        searchData() {
            fetch('/api/link_interface', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.filters)
            })
            .then(response => response.json())
            .then(data => {
                this.data = data;
            })
            .catch(error => console.error('Error:', error));
        },
        resetFilters() {
            this.filters = {
                ip: '',
                userId: '',
                phone: '',
                marketingLimit: '',
                greetingLimit: '',
                riskLimit: '',
                provinceFilter: '',
                selectedProvinces: []
            };
            this.selectAll = false;
            this.selectedRows = [];
            
            // 获取所有数据展示
            this.loadAllData();
        },
        exportData() {
            fetch('/api/export_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ selectedRows: this.selectedRows })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Data exported:', data);
            })
            .catch(error => console.error('Error:', error));
        },
        loadAllData() {
            fetch('/api/list_all')
            .then(response => response.json())
            .then(data => {
                this.data = data;
            })
            .catch(error => console.error('Error:', error));
        },
        previousPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
            }
        },
        nextPage() {
            if (this.currentPage * this.itemsPerPage < this.filteredData.length) {
                this.currentPage++;
            }
        },
        mounted() {
            this.loadAllData();  // 页面加载时自动加载所有数据
        }
    }
});
