import { postJson } from "./comm";
import {get_active_and_trimmed_code} from "./app";

export async function saveMicrobit(level:number){

      const response = await postJson("/generate_microbit_files",{
          level,
          code: get_active_and_trimmed_code()
      });
      if (response.filename) {
          window.location.replace("/download_microbit_files/");
      }
  }

