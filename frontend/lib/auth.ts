import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import Google from "next-auth/providers/google";
import { apiFetch } from "@/lib/api";

export interface BackendUser {
  id: string;
  name: string | null;
  email: string | null;
  image: string | null;
}

export const { handlers, signIn, signOut, auth } = NextAuth({
  pages: {
    signIn: "/sign-in",
  },
  session: { strategy: "jwt" },
  providers: [
    Google,
    Credentials({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        const email = credentials?.email as string | undefined;
        const password = credentials?.password as string | undefined;

        if (!email || !password) return null;

        const { data, error } = await apiFetch<BackendUser>("/auth/login", {
          method: "POST",
          body: JSON.stringify({ email, password }),
        });

        if (error || !data) return null;

        return {
          id: data.id,
          name: data.name,
          email: data.email,
          image: data.image,
        };
      },
    }),
  ],
  callbacks: {
    async signIn({ user, account, profile }) {
      // When a user signs in with Google, sync the account to the FastAPI backend
      if (account?.provider === "google" && profile?.email) {
        const { data, error } = await apiFetch<BackendUser>("/auth/google", {
          method: "POST",
          body: JSON.stringify({
            email: profile.email,
            name: profile.name ?? null,
            image: (profile as Record<string, unknown>).picture ?? null,
            provider: "google",
            provider_account_id: account.providerAccountId,
            access_token: account.access_token ?? null,
            refresh_token: account.refresh_token ?? null,
            expires_at: account.expires_at ?? null,
            token_type: account.token_type ?? null,
            scope: account.scope ?? null,
            id_token: account.id_token ?? null,
          }),
        });

        if (error || !data) return false;

        // Attach the backend user id so the jwt callback can use it
        user.id = data.id;
      }
      return true;
    },
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.name = user.name;
        token.email = user.email;
        token.picture = user.image;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.name = token.name as string;
        session.user.email = token.email as string;
        session.user.image = token.picture as string | undefined;
      }
      return session;
    },
  },
});
