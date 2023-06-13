<!--
<template>
    <div>
        <form v-on:submit.prevent="onSubmit" @submit="generateShortLink">
            <input v-model="mainLink" type="url" placeholder="https://example.com" pattern="https://.*" required>
            <input type="submit" value="Создать короткую ссылку"/>
        </form>
        <div v-if="shortLink">
            <input type="text" :value="shortLink" readonly>
            <button @click="copyToClipboard">Копировать</button>
        </div>
        <div>
          <img :src="screenshot" alt="screenshot"/>
        </div>
    </div>
</template>
-->

<template>
    <div>      
        <h1 class="mb-5 mt-5 text-center">Сервис сокращения ссылок</h1>  
        <b-form class="mb-5 text-center" inline @submit.prevent="generateShortLink">                    
            <label class="sr-only" for="input-link">Ваша ссылка:</label>
            <b-form-input class="mb-2 ms-2 me-2 w-50" id="input-link" v-model="mainLink" type="url" placeholder="https://example.com" pattern="https://.*" style="display: inline; width: auto; vertical-align: middle;" required></b-form-input>
            <b-button class="mb-2" type="submit" variant="primary">Создать короткую ссылку</b-button>                
        </b-form>
        <div class="mb-3 text-center">
            <div v-if="isFetching">
                <b-spinner></b-spinner>
            </div>
            <b-form inline v-if="shortLink">
                <label class="sr-only" for="shorted-link">Короткая ссылка:</label>
                <b-form-input class="mb-2 ms-2 me-2 w-50" id="shorted-link" type="text" :value="shortLink" readonly style="display: inline; width: auto; vertical-align: middle;"></b-form-input>
                <b-button class="mb-2" id="copy-btn" @click="copyToClipboard" data-clipboard-target="#shorted-link">{{isCopied}}</b-button>
            </b-form>        
        </div>
        <div v-if="shortLink" class="text-center">            
            <b-img v-if="screenshot" class="w-75" :src="screenshot" alt="Screenshot" fluid thumbnail></b-img>
            <div v-else>
                <b-spinner></b-spinner>
            </div>
        </div>
    </div>
</template>

<script>
    import ClipboardJS from 'clipboard';    

    export default {
        data() {
        return {        
            mainLink: '',
            shortLink: '',
            screenshot: null,
            isCopied: "Копировать",
            isFetching: false
        }
    },
    methods: {        
        generateShortLink() { 
            this.isFetching=true;   
            this.shortLink = '';
            this.screenshot = null;            
            this.checkValidUrl(this.mainLink).then(resp =>{
                if(resp===true){      
                    fetch(
                        //'http://192.168.3.2:8080/send',
                        '/send',
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type':'application/json'
                            },
                            body: JSON.stringify({mainLink:this.mainLink})
                        })
                        .then(resp => resp.json()) 
                        .then(data => {
                        //this.shortLink = 'http://192.168.3.2:3000/r/'+data.shortlink;               
                        this.shortLink = 'https://link-shortener-production-0bf0.up.railway.app/r/'+data.shortlink;
                        this.putImage(data.id)
                        })                      
                        .catch(error => console.log(error))     
                        
                        this.isCopied = "Копировать";
                        this.isFetching = false;       
                }else{
                    this.isFetching=false;
                } 
            })                
      },
      putImage(id){
        fetch(
            //`http://192.168.3.2:8080/putimage/${id}`,
            `/putimage/${id}`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify(''),
                timeout: 60000
            })
            .then(resp => resp.blob())
            .then(blob => {
              this.screenshot = URL.createObjectURL(blob)
            })  
            .catch(error => console.log(error))      
      },
      copyToClipboard() {
        new ClipboardJS('#copy-btn');
        this.isCopied = "Скопировано";                
      },
      checkValidUrl(url){               
        return fetch(url, {mode: "no-cors"})        
        .then(response => {                       
            if (response) {                                                
                return true;                
            } else {                
                alert("Ошибка: эта ссылка никуда не ведет");                
                return false;
            }})    
        .catch(() => {            
            alert("Ошибка: эта ссылка никуда не ведет");            
            return false;
        });                
    }
  }
}
</script>