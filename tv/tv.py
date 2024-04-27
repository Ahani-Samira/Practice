class TV:  
    def __init__(self):
        self.isOn = False
        self.isMuted = False
        self.currentChannelIndex = 0
        self.channelsList = self.search_channel()
        self.volume = 10
        self.MAX_VOLUME = 20

    def search_channel(self):
        '''
        ...search_channel...
        '''
        # TODO: Get from CABLE!
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 25]
    
    def power(self):
        '''
        You can turn the TV on or off.
        '''
        self.isOn = not self.isOn

    # Methods to be implemented :
    
    def volume_up(self):
        '''
        You can turn up the volume of the TV to {self.MAX_VOLUME}.
        '''
        if self.volume < self.MAX_VOLUME:
            self.volume += 1

    def volume_down(self):
        '''
        You can turn down the volume of the TV to 0.
        '''
        if self.volume > 0:
            self.volume -= 1

    def channel_up(self):
        '''
        ...
        '''
        if self.currentChannelIndex < len(self.channelsList)-1:
            self.currentChannelIndex += 1
        else:
            self.currentChannelIndex = 0

    def channel_down(self):
        '''
        ...
        '''
        if self.currentChannelIndex > 0:
            self.currentChannelIndex -= 1
        else:
            self.currentChannelIndex = len(self.channelsList)-1

    def set_channel(self, number):
        '''
        go to ...
        '''
        if number in self.channelsList:
            self.currentChannelIndex = self.channelsList.index(number)
            
    info = dir()
    def show_info(self):      
        if self.isOn == True :
            #print(help(TV))
            for it in self.info:
                if it[0] != '_' :
                    print(it)
        else:
            print("What do you expect from a TV that's turned off?!!")
                  
     
tv_23inch = TV()
tv = TV()

