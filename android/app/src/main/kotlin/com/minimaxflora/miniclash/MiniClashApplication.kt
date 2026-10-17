package com.minimaxflora.miniclash

import android.app.Application
import android.content.Context
import com.minimaxflora.miniclash.common.GlobalState

class MiniClashApplication : Application() {
    override fun attachBaseContext(base: Context?) {
        super.attachBaseContext(base)
        GlobalState.init(this)
    }
}
