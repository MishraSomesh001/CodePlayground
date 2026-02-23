import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";
import { signOutAction } from "@/lib/actions/auth";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export default async function DashboardPage() {
  const session = await auth();

  if (!session?.user) {
    redirect("/sign-in");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Dashboard</CardTitle>
          <CardDescription>
            You are signed in as{" "}
            <span className="font-medium">{session.user.name ?? session.user.email}</span>
          </CardDescription>
        </CardHeader>

        <CardContent className="space-y-4">
          <div className="rounded-md border p-4 text-sm space-y-1">
            <p>
              <span className="text-muted-foreground">ID:</span> {session.user.id}
            </p>
            <p>
              <span className="text-muted-foreground">Name:</span>{" "}
              {session.user.name ?? "—"}
            </p>
            <p>
              <span className="text-muted-foreground">Email:</span>{" "}
              {session.user.email ?? "—"}
            </p>
          </div>

          <form action={signOutAction}>
            <Button type="submit" variant="outline" className="w-full">
              Sign out
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
