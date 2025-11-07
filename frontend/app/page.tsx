"use client"

import { Thread } from "@/components/assistant-ui/thread";

export default function Page() {    
   const newSessionId = crypto.randomUUID();
  
    // 2. Store the new ID in sessionStorage for the duration of this specific page load.
    //    Even if you refresh, the code runs again, overwriting the old ID.
    sessionStorage.setItem('simpleSessionId', newSessionId);
  
  return <Thread />;
}