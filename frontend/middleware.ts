import { auth } from "@/lib/auth";
import { NextResponse } from "next/server";

const publicRoutes = ["/sign-in", "/sign-up"];
const authApiPrefix = "/api/auth";

export default auth((req) => {
  const { nextUrl } = req;
  const isLoggedIn = !!req.auth;

  // Always allow NextAuth API routes
  if (nextUrl.pathname.startsWith(authApiPrefix)) {
    return NextResponse.next();
  }

  const isPublic = publicRoutes.includes(nextUrl.pathname);

  // Redirect authenticated users away from auth pages
  if (isLoggedIn && isPublic) {
    return NextResponse.redirect(new URL("/dashboard", nextUrl));
  }

  // Redirect unauthenticated users to sign-in
  if (!isLoggedIn && !isPublic && nextUrl.pathname !== "/") {
    return NextResponse.redirect(new URL("/sign-in", nextUrl));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ["/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)"],
};
