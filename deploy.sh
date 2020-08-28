cd frontend || exit

# Build frontend
yarn build

# Move files to build root
mkdir -p build/root
for file in $(ls build | grep -E -v 'index\.html|static|root'); do
  mv "build/$file" build/root
done

cd ..
cd backend || exit

# Create venv if not exists
if [ -d "$DIRECTORY" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt

python3 manage.py collectstatic
waitress-serve todolist.wsgi:application
