import { QueryClientProvider } from "@tanstack/react-query";
import { closedQueryClient } from "./store/closedQueryClient";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <QueryClientProvider client={closedQueryClient}>
      <Component {...pageProps} />
    </QueryClientProvider>
  );
}
