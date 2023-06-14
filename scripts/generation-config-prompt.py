import modules.scripts as scripts
import gradio as gr

class GenarationConfigPrompt(scripts.Script):  
    def title(self):
        return self.__class__.__name__
    
    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion(self.title(), open=False):
            with gr.Row():
                with gr.Column(min_width = 50, scale=1):
                    trigger = gr.Textbox(
                        label="Triger Word",
                        lines=1,
                        value="config",
                        interactive =True,
                        elem_id="genconfprompt_trigger_word"
                    )
                    
        return [trigger]
    
    def before_process_batch(self, p, trigger, *args, **kwargs):
        extra = p.parse_extra_network_prompts()
        configs = extra.get(trigger)
        
        if (configs is None):
            return

        for config in configs:
            if len(config.positional) == 0:
                continue
            
            class ConfigProcessor:
                def swap():
                    p.width, p.height = p.height, p.width
                def set():
                    for key, val in config.named.items():
                        if not hasattr(p, key):
                            continue
                        setattr(p, key, type(getattr(p, key))(val))
            
            funcname = config.positional[0]
            if not hasattr(ConfigProcessor, funcname):
                continue
            
            func = getattr(ConfigProcessor, funcname)
            if not callable(func):
                continue
            
            func()
